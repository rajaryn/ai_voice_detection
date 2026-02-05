import torch
import librosa
import numpy as np
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor
import sys

# --- CONFIGURATION ---
MODEL_NAME = "MelodyMachine/Deepfake-audio-detection-V2"
# UPDATE THESE PATHS TO YOUR REAL FILES
PATH_TO_HUMAN_AUDIO = "clip1.mp3"  
PATH_TO_AI_AUDIO = "clip2.mp3"

def test_file(filepath, expected_type):
    print(f"\nAnalyzing {expected_type} file: {filepath}")
    
    try:
        # Load & Resample
        audio, _ = librosa.load(filepath, sr=16000)
        
        # Load Model
        extractor = AutoFeatureExtractor.from_pretrained(MODEL_NAME)
        model = AutoModelForAudioClassification.from_pretrained(MODEL_NAME)
        
        # Predict
        inputs = extractor(audio, sampling_rate=16000, return_tensors="pt", padding=True)
        with torch.no_grad():
            logits = model(**inputs).logits
            
        probs = torch.softmax(logits, dim=-1)
        pred_id = torch.argmax(logits, dim=-1).item()
        confidence = probs[0][pred_id].item()
        
        # Get raw label from config
        raw_label = model.config.id2label[pred_id]
        
        print(f"  -> Model Predicted ID: {pred_id}")
        print(f"  -> Model Predicted Label: '{raw_label}'")
        print(f"  -> Confidence: {confidence:.4f}")
        
        return pred_id, raw_label
        
    except FileNotFoundError:
        print(f"  [ERROR] File not found: {filepath}")
        return None, None
    except Exception as e:
        print(f"  [ERROR] Analysis failed: {e}")
        return None, None

def main():
    print(f"=== CALIBRATION TOOL FOR {MODEL_NAME} ===")
    
    # 1. Test Human
    human_id, human_label = test_file(PATH_TO_HUMAN_AUDIO, "HUMAN")
    
    # 2. Test AI
    ai_id, ai_label = test_file(PATH_TO_AI_AUDIO, "AI")
    
    print("\n=== CALIBRATION RESULTS ===")
    
    if human_id is None or ai_id is None:
        print("❌ Could not complete test. Check file paths.")
        return

    if human_id == ai_id:
        print("⚠️  WARNING: The model predicted the SAME class for both files.")
        print("   This means either:")
        print("   1. The model is not working well for these specific clips.")
        print("   2. One of your clips is too noisy or silent.")
        print("   Try using longer, clearer audio samples.")
    else:
        print("✅ SUCCESS: The model distinguishes the files.")
        print(f"   ID {human_id} ({human_label}) = HUMAN")
        print(f"   ID {ai_id} ({ai_label}) = AI")
        
        # Validation Check against Classifier Logic
        if "fake" in str(ai_label).lower() or "spoof" in str(ai_label).lower() or str(ai_label).lower() == "label_0":
            print("\n   [OK] The default logic in classifier.py matches these results.")
        else:
            print("\n   [ATTENTION] You need to update classifier.py logic!")
            print(f"   Ensure that ID {ai_id} maps to 'AI_GENERATED'.")

if __name__ == "__main__":
    main()