import sentry_sdk
from loguru import logger

from server.utils.error import generate_error


async def handle_exception(ex, message="An error occurred", status_code=500):
    logger.exception(ex)
    sentry_sdk.capture_exception(ex)
    return await generate_error(message, status_code=status_code)