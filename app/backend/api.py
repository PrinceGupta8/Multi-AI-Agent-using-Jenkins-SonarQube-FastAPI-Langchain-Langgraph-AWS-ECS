from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from app.common import logger
from app.common.custom_exception import CustomException
from app.config.settings import settings
from app.core.ai_agent import get_response_from_ai_agent

logger = logger.get_logger(__name__)
app = FastAPI(title="Multi AI Agent")

class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    message: List[str]
    allow_search: bool

@app.post("/chat")
def chat_endpoint(request: RequestState):
    logger.info(f"Received request for model: {request.model_name}")

    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning("Invalid model name")
        raise HTTPException(status_code=400, detail="Invalid model name")
    
    try:
        response = get_response_from_ai_agent(
            llm_id=request.model_name,
            query=request.message,
            allow_search=request.allow_search,
            system_prompt=request.system_prompt
        )
        logger.info(f"Successfully got response from AI Agent {request.model_name}")
        return {"response": response}

    except Exception as e:
        logger.error(f"Error during AI response generation: {str(e)}")
        # Wrap original exception for debugging but return generic message to client
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get AI response: {str(e)}"
        )
