from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

# Usuario y contraseña para desarrollo
# EN PRODUCCIÓN: Usar variables de entorno
DEVELOPMENT_USERS = {
    "admin": "tradingbot123",
    "trader": "password123"
}

def authenticate_bot(credentials: HTTPBasicCredentials = Depends(security)):
    """Autenticación básica para endpoints del bot"""
    
    # Verificar usuario existe
    if credentials.username not in DEVELOPMENT_USERS:
        raise HTTPException(
            status_code=401,
            detail="Usuario no autorizado",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    # Verificar contraseña (comparación segura contra timing attacks)
    correct_password = secrets.compare_digest(
        credentials.password.encode('utf-8'),
        DEVELOPMENT_USERS[credentials.username].encode('utf-8')
    )
    
    if not correct_password:
        raise HTTPException(
            status_code=401,
            detail="Contraseña incorrecta",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username

# Función simple para verificar tokens API (para el futuro)
def verify_api_key(api_key: str = None):
    """Verificación básica de API key"""
    if not api_key:
        raise HTTPException(status_code=401, detail="API key requerida")
    
    # Aquí iría la lógica para verificar API keys en base de datos
    # Por ahora retorna True si existe cualquier key
    return api_key is not None