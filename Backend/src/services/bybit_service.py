"""
Servicio Bybit
---------------
Actualmente el sistema está en modo SIMULADO usando `BybitMock`.
Para conectar con la API real, descomenta la clase `BybitTrading`
y crea tus claves en el archivo .env (BYBIT_API_KEY, BYBIT_API_SECRET).
"""

import random
import asyncio
from utils.logger import get_logger

logger = get_logger(__name__)

# ------------------------------------------------------
# 🧠 Cliente simulado para desarrollo (modo seguro)
# ------------------------------------------------------
class BybitMock:
    """Simulación del cliente Bybit para desarrollo local."""

    async def get_market_data(self, symbol="BTCUSDT"):
        """Devuelve datos de mercado falsos (simulados)."""
        price = round(random.uniform(30000, 70000), 2)
        logger.info(f"[MOCK] get_market_data {symbol} -> {price}")
        return {"close": [price], "high": [price], "low": [price], "volume": [100]}

    async def place_order(self, symbol, side, qty, price=None, stop_loss=None, take_profit=None):
        """Simula la colocación de una orden sin ejecutar nada real."""
        logger.info(f"[MOCK] place_order: {symbol=} {side=} {qty=} {price=} {stop_loss=} {take_profit=}")
        await asyncio.sleep(0.2)
        return {"ret_code": 0, "result": {"order_id": f"mock-{random.randint(1000,9999)}"}}

# Instancia global activa (modo mock)
bybit_client = BybitMock()

# ------------------------------------------------------
# 🔒 Futuro código real (mantener comentado por ahora)
# ------------------------------------------------------

# from pybit import HTTP
# import pandas as pd
# from typing import Dict, List, Optional
# from config import settings

# class BybitTrading:
#     """Cliente real para interactuar con Bybit API."""
#     def __init__(self):
#         self.session = None
#         self.connect()
    
#     def connect(self):
#         """Conectar a Bybit API."""
#         try:
#             self.session = HTTP(
#                 endpoint="https://api-testnet.bybit.com" if settings.BYBIT_TESTNET else "https://api.bybit.com",
#                 api_key=settings.BYBIT_API_KEY,
#                 api_secret=settings.BYBIT_API_SECRET
#             )
#             logger.info("✅ Conectado a Bybit API")
#         except Exception as e:
#             logger.error(f"❌ Error conectando a Bybit: {e}")
    
#     async def get_account_balance(self) -> Dict:
#         """Obtener balance de la cuenta."""
#         try:
#             balance = self.session.get_wallet_balance(coin="USDC")
#             return balance
#         except Exception as e:
#             logger.error(f"Error obteniendo balance: {e}")
#             return {}
    
#     async def get_market_data(self, symbol: str, interval: str = "1", limit: int = 100) -> pd.DataFrame:
#         """Obtener datos de mercado OHLCV."""
#         try:
#             kline = self.session.query_kline(symbol=symbol, interval=interval, limit=limit)
#             df = pd.DataFrame(kline['result'])
#             return df
#         except Exception as e:
#             logger.error(f"Error obteniendo market data: {e}")
#             return pd.DataFrame()
    
#     async def place_order(self, symbol: str, side: str, order_type: str, qty: float, 
#                          price: Optional[float] = None, stop_loss: Optional[float] = None,
#                          take_profit: Optional[float] = None) -> Dict:
#         """Colocar orden en Bybit."""
#         try:
#             order_params = {
#                 "symbol": symbol,
#                 "side": side,
#                 "order_type": order_type,
#                 "qty": str(qty),
#                 "time_in_force": "GoodTillCancel"
#             }
#             if price:
#                 order_params["price"] = str(price)
#             if stop_loss:
#                 order_params["stop_loss"] = str(stop_loss)
#             if take_profit:
#                 order_params["take_profit"] = str(take_profit)
#             result = self.session.place_active_order(**order_params)
#             return result
#         except Exception as e:
#             logger.error(f"Error colocando orden: {e}")
#             return {}

#     async def get_open_orders(self, symbol: str) -> List[Dict]:
#         """Obtener órdenes abiertas."""
#         try:
#             orders = self.session.get_active_order(symbol=symbol)
#             return orders.get('result', {}).get('data', [])
#         except Exception as e:
#             logger.error(f"Error obteniendo órdenes abiertas: {e}")
#             return []

#     async def cancel_order(self, symbol: str, order_id: str) -> bool:
#         """Cancelar orden específica."""
#         try:
#             result = self.session.cancel_active_order(symbol=symbol, order_id=order_id)
#             return result['ret_code'] == 0
#         except Exception as e:
#             logger.error(f"Error cancelando orden: {e}")
#             return False

#     async def get_position(self, symbol: str) -> Dict:
#         """Obtener posición actual."""
#         try:
#             position = self.session.my_position(symbol=symbol)
#             return position.get('result', {})
#         except Exception as e:
#             logger.error(f"Error obteniendo posición: {e}")
#             return {}

# # Cuando tengas las claves, reemplaza la instancia:
# # bybit_client = BybitTrading()
