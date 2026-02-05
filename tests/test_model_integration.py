import numpy as np
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.classifier import classifier

def test_prediction():
    print("Generating dummy audio (16kHz, 2 seconds)...")
    sr = 16000
    duration = 2
    # Generate white noise
    audio_data = np.random.uniform(-1, 1, sr * duration).astype(np.float32)
    
    print("Running prediction...")
    try:
        label, confidence, explanation = classifier.predict(audio_data, "en")
        print("\n--- Prediction Result ---")
        print(f"Label: {label}")
        print(f"Confidence: {confidence}")
        print(f"Explanation: {explanation}")
        print("-------------------------")
    except Exception as e:
        print(f"Prediction failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_prediction()
