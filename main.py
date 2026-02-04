from fastapi import FastAPI
from api.routes import router
import uvicorn

app = FastAPI(
    title="AI Voice Detection API",
    description="API to detect AI-generated voices in Tamil, English, Hindi, Malayalam, and Telugu.",
    version="1.0.0"
)

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "AI Voice Detection API is running. Use /api/voice-detection to analyze audio."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
