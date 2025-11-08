from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status
from utils.logger import get_logger

logger = get_logger("exception_handler")

async def http_exception_handler(request: Request, exc):
    logger.error(f"HTTP error: {exc}")
    return JSONResponse(
        status_code=getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR),
        content={"detail": str(exc)}
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )
#Añadir middleware global de captura de errores y un handler unificado