import requests
import base64
import os
import json

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000/api/voice-detection"
API_KEY = "sk_test_123456789"  # Must match the key in your .env or core/config.py

def encode_file_to_base64(file_path):
    """Reads a file and converts it to a Base64 string."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    with open(file_path, "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')
    return encoded_string

def check_api_with_file(file_path, language="English"):
    print(f"\n--- Testing API with file: {os.path.basename(file_path)} ---")
    
    try:
        # 1. Prepare Data
        print("1. Encoding audio...")
        audio_b64 = encode_file_to_base64(file_path)
        
        # 2. Construct Payload
        # NOTE: 'language' is required by your Pydantic schema
        payload = {
            "audioBase64": audio_b64,
            "language": language 
        }
        
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }

        # 3. Send Request
        print(f"2. Sending request to {API_URL}...")
        response = requests.post(API_URL, json=payload, headers=headers)

        # 4. Print Results
        print(f"3. Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("\n✅ SUCCESS! API Response:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("\n❌ ERROR! Server Response:")
            print(response.text)

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Is it running? (uvicorn main:app --reload)")
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    
    real_mp3_path = "clip2.mp3" 
    
    # You can also change the language if testing Hindi/Tamil/etc.
    check_api_with_file(real_mp3_path, language="Hindi")