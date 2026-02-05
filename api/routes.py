from fastapi import APIRouter, Depends, HTTPException
from api.schemas import VoiceAnalysisRequest, VoiceAnalysisResponse
from api.dependencies import get_api_key
from core.audio import decode_audio
from core.classifier import classifier
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/voice-detection", response_model=VoiceAnalysisResponse, dependencies=[Depends(get_api_key)])
async def analyze_voice(request: VoiceAnalysisRequest):
    logger.info(f"Received voice analysis request for language: {request.language}")
    
    try:
        # 1. Decode Audio
        try:
            # ensure decode_audio returns the array AND the sample rate
            audio_array, sr = decode_audio(request.audioBase64)
        except ValueError as e:
            logger.error(f"Audio decoding failed: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid Audio Data: {str(e)}")
            
        # 2. Analyze Voice
        # CRITICAL FIX: Pass 'sr' (int), not 'request.language' (str)
        # The classifier needs 'sr' to check if resampling is needed.
        classification, confidence, explanation = classifier.predict(audio_array, source_sr=sr)
        
        # 3. Construct Response
        return VoiceAnalysisResponse(
            status="success",
            language=request.language, # Pass language through if needed for logging/response
            classification=classification,
            confidenceScore=confidence,
            explanation=explanation
        )

    except HTTPException:
        raise # Re-raise HTTP exceptions so FastAPI handles them correctly
        
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        # CRITICAL FIX: Do not return a partial VoiceAnalysisResponse here.
        # It will fail Pydantic validation if 'classification' is a required field.
        raise HTTPException(status_code=500, detail=str(e))