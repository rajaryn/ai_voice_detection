import requests
import base64
import json

# Constants
API_URL = "http://127.0.0.1:8000/api/voice-detection"
API_KEY = "sk_test_123456789"

def create_dummy_audio_base64():
    """
    Returns a Base64 string of a valid, short silent MP3 file (1 second).
    Generated using ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 1 -q:a 9 -acodec libmp3lame out.mp3
    """
    return "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU2LjM2LjEwMAAAAAAAAAAAAAAA//OEAAAAAAAAAAAAAAAAAAAAAAAASW5mbwAAAA8AAAAEAAABIADAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAw//OEAAABAAAAAgAAAADAAAAAAAAAAAAAAAAAAAAAAABMYXZjNTYuNjAuMTAwAAAAAAAAAAAAAAD/84QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJ=="

def run_test():
    print(f"Testing API at {API_URL}...")
    
    payload = {
        "language": "English",
        "audioFormat": "mp3",
        "audioBase64": create_dummy_audio_base64()
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        try:
            data = response.json()
            print("Response Body:")
            print(json.dumps(data, indent=2))
        except:
            print("Could not parse JSON response")
            print(response.text)
            
        if response.status_code == 200 and data.get("status") == "success":
            print("\n✅ Verification SUCCESS: API responded validly.")
        else:
            print("\n❌ Verification FAILED.")

    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to server. Is it running?")
        print("Run: 'uvicorn main:app --reload' in a separate terminal.")

if __name__ == "__main__":
    run_test()
