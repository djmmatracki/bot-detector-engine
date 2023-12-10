from fastapi import APIRouter
from dependencies import bot_detector
from schemas import RequestSample
import asyncio
import logging
logger = logging.getLogger()

router = APIRouter()

@router.post("/threat")
async def get_threat_score(request: RequestSample):
    logger.debug(f"Received requests with content {request}")
    network_model_task = bot_detector.verify_request(request)
    logger.debug(f"network model task for ip {request.remote_ip} is: {network_model_task}")
    if network_model_task:
        return {
            "threat": 1
        }

    if request.social_media_user is not None and len(request.content) != 0:
        user_model_task = bot_detector.verify_user(request.social_media_user)
        text_model_task = bot_detector.verify_text(request.content)
        text_model_result, user_model_result = await asyncio.gather(
            text_model_task, user_model_task
        )
        logger.debug(f"user model task for ip {request.remote_ip} is: {user_model_result}")
        logger.debug(f"text model task for ip {request.remote_ip} is: {text_model_result}")
        return {
            "threat": text_model_result * user_model_result,
            "text_threat": text_model_result,
            "user_threat": user_model_result,
        }

    if request.social_media_user is not None:
        user_model_result = await bot_detector.verify_user(request.social_media_user)
        logger.debug(f"user model task for ip {request.remote_ip} is: {user_model_result}")
        return {
            "threat": user_model_result
        }
    
    if len(request.content) != 0:
        text_model_result = await bot_detector.verify_text(request.content)
        logger.debug(f"text model task for ip {request.remote_ip} is: {text_model_result}")
        return {
            "threat": text_model_result
        }
    logger.debug("threat returned 0")

    return {
        "threat": 0
    }
