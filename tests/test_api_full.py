import requests
import base64
import numpy as np
import json
import time
import io
import soundfile as sf # You might need to install soundfile: pip install soundfile

def create_dummy_audio_base64():
    """Generates a short segment of white noise and returns it as base64 string."""
    sr = 16000
    duration = 1.0 # seconds
    audio = np.random.uniform(-0.5, 0.5, int(sr * duration))
    
    # Save to memory buffer as WAV/MP3
    buffer = io.BytesIO()
    sf.write(buffer, audio, sr, format='WAV')
    buffer.seek(0)
    
    # Encode to base64
    audio_b64 = base64.b64encode(buffer.read()).decode('utf-8')
    return audio_b64

def test_api():
    url = "http://127.0.0.1:8000/api/voice-detection"
    print(f"Testing API at {url}...")
    
    # Generate dummy audio
    print("Generating dummy audio...")
    try:
        audio_b64 = create_dummy_audio_base64()
    except Exception as e:
        print(f"Error creating dummy audio (ensure 'soundfile' and 'numpy' are installed): {e}")
        return

    payload = {
        "audioBase64": audio_b64,
        "language": "English"
    }

    # API Key - Using default from core/config.py
    headers = {
        "x-api-key": "sk_test_123456789" 
    }

    print("Sending request... (Will retry if server is starting up)")
    
    max_retries = 10
    for attempt in range(max_retries):
        try:
            start_time = time.time()
            response = requests.post(url, json=payload, headers=headers)
            duration = time.time() - start_time
            
            print(f"\nResponse Status: {response.status_code}")
            print(f"Time Taken: {duration:.2f}s")
            
            if response.status_code == 200:
                print("\nResponse Body:")
                print(json.dumps(response.json(), indent=2))
            else:
                print("Error Response:")
                print(response.text)
            return # Success or server error, stop retrying

        except requests.exceptions.ConnectionError:
            print(f"Attempt {attempt+1}/{max_retries}: Could not connect to API. Server might be starting/downloading model...")
            time.sleep(5) # Wait 5 seconds before retrying
    
    print("\n[ERROR] Failed to connect after multiple attempts.")
    print("Ensure 'uvicorn main:app --reload' is running and the model download has finished.")

if __name__ == "__main__":
    test_api()
