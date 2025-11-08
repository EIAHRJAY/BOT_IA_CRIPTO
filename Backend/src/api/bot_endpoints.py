from fastapi import APIRouter, Depends
from security.auth import authenticate_bot
from services.trading_service import start_trading_loop, stop_trading_loop
from utils.logger import get_logger

router = APIRouter()

logger = get_logger(__name__)

@router.get("/")
def read_root():
    """Endpoint raíz: verificación inicial"""
    return {"message": "✅ FINALMENTE FUNCIONA", "status": "active"}

@router.get("/health")
def health_check():
    """Verifica el estado de salud del servicio"""
    return {"status": "healthy"}

# 🔐 Endpoints protegidos por autenticación
@router.get("/bot/status")
async def bot_status(username: str = Depends(authenticate_bot)):
    return {
        "message": f"🤖 Bot status - Usuario: {username}",
        "bot_running": False,
        "protected": True
    }

@router.post("/bot/start")
async def start_bot(username: str = Depends(authenticate_bot)):
    result = await start_trading_loop()
    logger.info(f"🟢 Bot iniciado por {username} -> {result}")
    return {
        "message": f"✅ Bot iniciado por: {username}",
        "status": result.get("status", "running")
    }

@router.post("/bot/stop")
async def stop_bot(username: str = Depends(authenticate_bot)):
     result = await stop_trading_loop()
     logger.info(f"🔴 Bot detenido por {username} -> {result}")
     return {
         "message": f"🛑 Bot detenido por: {username}", 
         "status": result.get("status", "stopped")
         }