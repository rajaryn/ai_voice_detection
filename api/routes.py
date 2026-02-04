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
            audio_array, sr = decode_audio(request.audioBase64)
        except ValueError as e:
            logger.error(f"Audio decoding failed: {e}")
            raise HTTPException(status_code=400, detail=str(e))
            
        # 2. Analyze Voice
        label, confidence, explanation = classifier.predict(audio_array, request.language)
        
        # 3. Construct Response
        return VoiceAnalysisResponse(
            status="success",
            language=request.language,
            classification=label,
            confidenceScore=confidence,
            explanation=explanation
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        return VoiceAnalysisResponse(
            status="error",
            message=str(e)
        )
