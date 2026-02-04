# AI Voice Detection API

A FastAPI-based REST API to detect AI-generated voices in Tamil, English, Hindi, Malayalam, and Telugu.

## 📂 Project Structure

```
D:\Projects\ai_voice_detection\
├── main.py              # Entry point
├── api/                 # API Routes, Schemas, Dependencies
├── core/                # Audio Processing & Classification Logic
├── tests/               # Verification Scripts
└── requirements.txt     # Dependencies
```

## 🚀 Setup & Run

1.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

    _Note: You need `ffmpeg` installed on your system for `librosa` to load MP3 files._

2.  **Run the Server**:

    ```bash
    uvicorn main:app --reload
    ```

    The API will be available at `http://127.0.0.1:8000`.

3.  **Test the Endpoint**:
    You can use the provided verification script or `curl`.

    **Using Verification Script:**

    ```bash
    python tests/verify_deployment.py
    ```

    **Using cURL:**

    ```bash
    curl -X POST http://127.0.0.1:8000/api/voice-detection \
      -H "Content-Type: application/json" \
      -H "x-api-key: sk_test_123456789" \
      -d '{
        "language": "English",
        "audioFormat": "mp3",
        "audioBase64": "<YOUR_BASE64_STRING>"
      }'
    ```

## ⚙️ Configuration

- **API Key**: Default is `sk_test_123456789`. Change in `core/config.py` or set `API_KEY_SECRET` env var.
- **Model**: Currently uses a **Placeholder/Dummy** classifier for demonstration. To use a real model, update `core/classifier.py`.
