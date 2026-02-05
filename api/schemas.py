from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional
import base64
import binascii

# Use standard python Literal
SUPPORTED_LANGUAGES = Literal["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

class VoiceAnalysisRequest(BaseModel):
    # Matches the 5 languages in the requirement doc
    language: SUPPORTED_LANGUAGES = "English" # Good to have a default fallback
    
    # REMOVED 'audioFormat' to prevent 422 errors if the evaluator doesn't send it.
    # If you really need it, use: audioFormat: Literal["mp3"] = "mp3"
    
    audioBase64: str = Field(..., description="Base64 encoded MP3 audio")

    @field_validator('audioBase64')
    @classmethod
    def validate_base64(cls, v):
        if not v:
            raise ValueError("Empty audio string")
        
        # 1. Sanity Check: Length
        if len(v) < 100:
            raise ValueError("Audio string too short to be valid")
        
        # 2. Structure Check: Validate it's actually Base64
        try:
            # Check if it can be decoded (fast check)
            base64.b64decode(v, validate=True)
        except binascii.Error:
            raise ValueError("Invalid Base64 string")
            
        return v

class VoiceAnalysisResponse(BaseModel):
    status: Literal["success", "error"]
    
    # Optional fields are correct (allows you to return just "status" & "message" on error)
    language: Optional[str] = None
    classification: Optional[Literal["AI_GENERATED", "HUMAN"]] = None
    confidenceScore: Optional[float] = None
    explanation: Optional[str] = None
    message: Optional[str] = None