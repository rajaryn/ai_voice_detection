import base64
import numpy as np
import tempfile
import os
import librosa

def decode_audio(base64_string: str) -> np.ndarray:
    """
    Decodes a Base64 string to a numpy array (audio series).
    """
    try:
        # Decode base64 string to bytes
        audio_bytes = base64.b64decode(base64_string)
        
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(audio_bytes)
            temp_path = temp_audio.name
        
        try:
            # Load audio using librosa
            # sr=16000 is crucial for Wav2Vec2 and deepfake detection models
            y, sr = librosa.load(temp_path, sr=16000)
            return y, sr
        finally:
            # Cleanup temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    except Exception as e:
        import traceback
        traceback.print_exc() # Print stack trace to server logs
        raise ValueError(f"Failed to process audio: {type(e).__name__} - {str(e)}")
