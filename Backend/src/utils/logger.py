import logging
import os
from datetime import datetime

# Crear carpeta de logs si no existe
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Nombre del archivo con fecha
log_filename = os.path.join(LOG_DIR, f"bot_{datetime.now().strftime('%Y-%m-%d')}.log")

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

# Logger principal del sistema
logger = logging.getLogger("trading_bot")

def get_logger(name: str = None):
    """Devuelve un logger con un nombre específico (por módulo o función)."""
    return logging.getLogger(name or "trading_bot")

# Mensaje de inicialización
logger.info("📄 Sistema de logs inicializado correctamente.")

# en src/utils/logger.py (al final)
# Redirigir uvicorn/fastapi a nuestro logger
# import logging
# for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
#     logging.getLogger(name).handlers = logging.getLogger("trading_bot").handlers
