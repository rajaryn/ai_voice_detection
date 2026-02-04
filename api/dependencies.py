from fastapi import Header, HTTPException, status
from core.config import API_KEY_SECRET

async def get_api_key(x_api_key: str = Header(..., description="API Key for authentication")):
    if x_api_key != API_KEY_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return x_api_key
