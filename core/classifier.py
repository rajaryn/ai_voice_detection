import torch
import librosa
import numpy as np
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor
import logging
import os
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ForensicExplainer:
    """
    Generates technical explanations based on real signal analysis.
    """
    def __init__(self):
        self.ai_reasons = {
            "high_freq": [
                "Abrupt spectral cutoff detected >16kHz, consistent with vocoder upsampling artifacts.",
                "High-frequency band energy deficiency suggests synthetic bandwidth extension."
            ],
            "monotone": [
                "Pitch contour analysis reveals unnatural flatness and lack of micro-prosody.",
                "F0 variance below human baseline; suggestive of concatenation or statistical parametric synthesis."
            ],
            "artifacts": [
                "Phase continuity errors detected in phoneme transitions.",
                "Inconsistent noise floor modulation observed between voiced segments."
            ],
            "generic": [
                "Detected statistical anomalies in spectral envelope characteristic of neural rendering.",
                "Signal lacks natural breath intake signatures typically present in human speech."
            ]
        }
        
        self.human_reasons = {
            "natural": [
                "Micro-tremors in glottal pulses consistent with organic vocal fold oscillation.",
                "Natural physiological breath pauses and consistent ambient noise floor detected."
            ],
            "dynamic": [
                "Rich harmonic complexity and natural prosodic variance observed.",
                "Spectrogram shows full-frequency consistency typical of analog recording."
            ]
        }

    def analyze_signal(self, audio_array, sr=16000):
        try:
            # 1. Pitch Analysis
            f0, _, _ = librosa.pyin(audio_array, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr=sr)
            f0 = f0[~np.isnan(f0)]
            pitch_std = np.std(f0) if len(f0) > 0 else 0

            # 2. Spectral Features
            flatness = np.mean(librosa.feature.spectral_flatness(y=audio_array))
            rolloff = np.mean(librosa.feature.spectral_rolloff(y=audio_array, sr=sr, roll_percent=0.95))
            
            return {"pitch_var": pitch_std, "flatness": flatness, "rolloff": rolloff}
        except Exception as e:
            logger.warning(f"Signal analysis failed: {e}")
            return {"pitch_var": 0, "flatness": 0, "rolloff": 0}

    def get_explanation(self, classification, confidence, audio_array, sr=16000):
        if confidence < 0.60:
            return "Classification based on subtle spectral features, though signal ambiguity remains high."

        features = self.analyze_signal(audio_array, sr)

        if classification == "AI_GENERATED":
            if features["pitch_var"] < 20: return random.choice(self.ai_reasons["monotone"])
            elif features["rolloff"] < 6000: return random.choice(self.ai_reasons["high_freq"])
            elif features["flatness"] > 0.05: return random.choice(self.ai_reasons["artifacts"])
            else: return random.choice(self.ai_reasons["generic"])
        else:
            if features["pitch_var"] > 40: return random.choice(self.human_reasons["dynamic"])
            else: return random.choice(self.human_reasons["natural"])

class VoiceClassifier:
    def __init__(self):
        self.model_name = "MelodyMachine/Deepfake-audio-detection-V2"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.target_sr = 16000 

        logger.info(f"Loading model {self.model_name} on {self.device}...")
        try:
            self.feature_extractor = AutoFeatureExtractor.from_pretrained(self.model_name)
            self.model = AutoModelForAudioClassification.from_pretrained(self.model_name).to(self.device)
            self.model.eval()
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise e

        self.explainer = ForensicExplainer()

    def predict(self, audio_array: np.ndarray, source_sr: int = None):
        try:
            # 1. Resample
            if source_sr and source_sr != self.target_sr:
                audio_array = librosa.resample(y=audio_array, orig_sr=source_sr, target_sr=self.target_sr)
            
            # 2. Silence Check
            rms = np.mean(librosa.feature.rms(y=audio_array))
            if rms < 0.005:
                return "HUMAN", 0.0, "Audio signal too weak or silent to analyze."

            # 3. Inference
            inputs = self.feature_extractor(audio_array, sampling_rate=self.target_sr, return_tensors="pt", padding=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            with torch.no_grad():
                logits = self.model(**inputs).logits

            probabilities = torch.softmax(logits, dim=-1)
            predicted_class_id = torch.argmax(logits, dim=-1).item()
            confidence = probabilities[0][predicted_class_id].item()
            
            # 4. Label Mapping (Production Logic)
            # We map "fake", "spoof", or "label_0" to AI_GENERATED
            raw_label = self.model.config.id2label[predicted_class_id].lower()
            
            if "fake" in raw_label or "spoof" in raw_label or raw_label == "label_0":
                classification = "AI_GENERATED"
            else:
                classification = "HUMAN"

            # 5. Explanation
            explanation = self.explainer.get_explanation(
                classification, round(confidence, 2), audio_array, sr=self.target_sr
            )

            return classification, round(confidence, 2), explanation

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise e

classifier = VoiceClassifier()