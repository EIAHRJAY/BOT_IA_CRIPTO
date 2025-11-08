from fastapi import FastAPI, HTTPException
from api.bot_endpoints import router as bot_router
from middleware.exception_handler import http_exception_handler, generic_exception_handler
from fastapi.exceptions import RequestValidationError
from utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Trading Bot Backend",
    description="API principal del cerebro del bot de trading (Bybit + IA + Telegram + n8n)",
    version="0.1.0",
)

# 🔗 Incluir rutas principales
# 🔗 Incluir rutas principales (solo las necesarias)
app.include_router(bot_router, prefix="/api", tags=["bot"])

#agregar middlewares o eventos de arranque aquí.
#todo error no capturado llegará a logger y 
#la API devolverá JSON consistente. Te evitará ver caídas raras sin rastro.
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
