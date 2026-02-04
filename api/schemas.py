from pydantic import BaseModel, Field, validator
from typing import Literal

SUPPORTED_LANGUAGES = Literal["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

class VoiceAnalysisRequest(BaseModel):
    language: SUPPORTED_LANGUAGES
    audioFormat: Literal["mp3"]
    audioBase64: str = Field(..., description="Base64 encoded MP3 audio")

    @validator('audioBase64')
    def validate_base64(cls, v):
        if not v or len(v) < 100:  # Basic sanity check
            raise ValueError("Invalid audioBase64 string")
        return v

class VoiceAnalysisResponse(BaseModel):
    status: Literal["success", "error"]
    language: str | None = None
    classification: Literal["AI_GENERATED", "HUMAN"] | None = None
    confidenceScore: float | None = None
    explanation: str | None = None
    message: str | None = None # For error messages
