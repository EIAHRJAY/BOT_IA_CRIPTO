import asyncio
from database import SessionLocal
from utils.logger import get_logger
from services.bybit_service import bybit_client

logger = get_logger(__name__)


class TradingBot:
    """Bot de trading básico en modo simulado."""
    def __init__(self, db):
        self.db = db
        self.is_running = False

    async def start_trading(self):
        """Loop principal del bot (simulado)."""
        self.is_running = True
        logger.info("🤖 TradingBot iniciado en modo simulación.")

        while self.is_running:
            try:
                market_data = await bybit_client.get_market_data("BTCUSDT")
                current_price = market_data["close"][-1]

                # Simulación simple de lógica
                if current_price < 40000:
                    decision = "BUY"
                elif current_price > 65000:
                    decision = "SELL"
                else:
                    decision = "HOLD"

                logger.info(f"📊 Precio: {current_price} | Decisión: {decision}")

                if decision in ["BUY", "SELL"]:
                    await bybit_client.place_order(
                        symbol="BTCUSDT",
                        side=decision,
                        qty=0.01,
                        price=current_price,
                    )

                await asyncio.sleep(5)

            except asyncio.CancelledError:
                logger.info("Trading loop cancelado correctamente.")
                break
            except Exception as e:
                logger.error(f"❌ Error en loop de trading: {e}")
                await asyncio.sleep(5)

        logger.info("🛑 Trading loop detenido.")


# ------------------------------
# Control global del bot
# ------------------------------

trading_bot = None
_trading_task = None


async def start_trading_loop():
    global trading_bot, _trading_task

    if trading_bot and trading_bot.is_running:
        logger.info("Trading bot ya estaba en ejecución")
        return {"status": "already_running"}

    db = SessionLocal()
    trading_bot = TradingBot(db)
    _trading_task = asyncio.create_task(trading_bot.start_trading())
    logger.info("Trading loop iniciado")
    return {"status": "running"}


async def stop_trading_loop():
    global trading_bot, _trading_task

    if not trading_bot or not trading_bot.is_running:
        logger.info("Trading bot no estaba en ejecución")
        return {"status": "not_running"}

    trading_bot.is_running = False
    if _trading_task:
        _trading_task.cancel()
        try:
            await _trading_task
        except asyncio.CancelledError:
            logger.info("Task de trading cancelada correctamente")

    logger.info("Trading loop detenido manualmente")
    return {"status": "stopped"}


__all__ = ["start_trading_loop", "stop_trading_loop", "TradingBot"]


# ===============================================================
# 🔮 FUTURO MÓDULO DE TRADING REAL (mantener como referencia)
# =============================================================== 
# try:
#     import pandas as pd
#     import ta
#     PANDAS_AVAILABLE = True
# except ImportError:
#     PANDAS_AVAILABLE = False
#     print("⚠️  Pandas/TA no disponibles - modo simulación")

# import asyncio
# from sqlalchemy.orm import Session
# from typing import Dict, List
# from datetime import datetime

# from models import Trade, TradingConfig, MarketData, AIDecision, Notification
# from config import settings
# from services.bybit_service import bybit_client

# class TradingBot:
#     def __init__(self, db: Session):
#         self.db = db
#         self.active_strategies = {}
#         self.is_running = False
    
#     async def start_trading(self):
#         """Iniciar el bot de trading"""
#         self.is_running = True
#         mode = "REAL" if PANDAS_AVAILABLE else "SIMULACIÓN"
#         print(f"🤖 Bot de trading iniciado - Modo: {mode}")
        
#         while self.is_running:
#             try:
#                 active_configs = self.db.query(TradingConfig).filter(
#                     TradingConfig.is_active == True
#                 ).all()
                
#                 for config in active_configs:
#                     await self.analyze_and_trade(config)
                
#                 await asyncio.sleep(60)
                
#             except Exception as e:
#                 print(f"Error en trading loop: {e}")
#                 await asyncio.sleep(300)
    
#     async def analyze_and_trade(self, config: TradingConfig):
#         """Analizar y ejecutar trades según la estrategia"""
#         try:
#             if not PANDAS_AVAILABLE:
#                 print(f"🔍 Simulando análisis de {config.symbol}")
#                 return
            
#             market_data = await bybit_client.get_market_data(config.symbol)
            
#             if market_data.empty:
#                 return
            
#             indicators = await self.calculate_indicators(market_data)
#             decision = await self.make_trading_decision(config, market_data, indicators)
            
#             if decision['action'] in ['BUY', 'SELL']:
#                 await self.execute_trade(config, decision, market_data)
                
#         except Exception as e:
#             print(f"Error en analyze_and_trade: {e}")
    
#     async def calculate_indicators(self, df: pd.DataFrame) -> Dict:
#         """Calcular indicadores técnicos"""
#         if not PANDAS_AVAILABLE:
#             return {}
            
#         try:
#             df['close'] = pd.to_numeric(df['close'])
#             df['high'] = pd.to_numeric(df['high'])
#             df['low'] = pd.to_numeric(df['low'])
#             df['volume'] = pd.to_numeric(df['volume'])
            
#             rsi = ta.momentum.RSIIndicator(df['close']).rsi()
#             macd = ta.trend.MACD(df['close'])
#             sma_20 = ta.trend.SMAIndicator(df['close'], window=20).sma_indicator()
#             sma_50 = ta.trend.SMAIndicator(df['close'], window=50).sma_indicator()
#             bollinger = ta.volatility.BollingerBands(df['close'])
            
#             return {
#                 'rsi': rsi.iloc[-1],
#                 'macd': macd.macd().iloc[-1],
#                 'macd_signal': macd.macd_signal().iloc[-1],
#                 'sma_20': sma_20.iloc[-1],
#                 'sma_50': sma_50.iloc[-1],
#                 'bb_upper': bollinger.bollinger_hband().iloc[-1],
#                 'bb_lower': bollinger.bollinger_lband().iloc[-1],
#                 'bb_middle': bollinger.bollinger_mavg().iloc[-1]
#             }
#         except Exception as e:
#             print(f"Error calculando indicadores: {e}")
#             return {}
    
#     async def make_trading_decision(self, config: TradingConfig, market_data: pd.DataFrame, 
#                                   indicators: Dict) -> Dict:
#         """Tomar decisión de trading basada en la estrategia"""
#         if not PANDAS_AVAILABLE:
#             return {'action': 'HOLD', 'reason': 'Modo simulación'}
            
#         current_price = float(market_data['close'].iloc[-1])
        
#         if config.strategy_name == "GRID":
#             return await self.grid_strategy(config, current_price, indicators)
#         elif config.strategy_name == "TRAILING_STOP":
#             return await self.trailing_stop_strategy(config, current_price, indicators)
#         elif config.strategy_name == "RANGE_BOUND":
#             return await self.range_bound_strategy(config, current_price, indicators)
#         else:
#             return {'action': 'HOLD', 'reason': 'No strategy matched'}
    
#     async def grid_strategy(self, config: TradingConfig, current_price: float, 
#                           indicators: Dict) -> Dict:
#         """Estrategia Grid Trading"""
#         try:
#             grid_levels = config.grid_levels
#             price_range = config.price_range_max - config.price_range_min
#             grid_step = price_range / grid_levels
            
#             current_level = int((current_price - config.price_range_min) / grid_step)
            
#             if current_level <= grid_levels * 0.3:
#                 return {
#                     'action': 'BUY',
#                     'reason': f'Grid level {current_level} - Zona de compra',
#                     'price': current_price,
#                     'quantity': config.max_position_size / grid_levels
#                 }
#             elif current_level >= grid_levels * 0.7:
#                 return {
#                     'action': 'SELL', 
#                     'reason': f'Grid level {current_level} - Zona de venta',
#                     'price': current_price,
#                     'quantity': config.max_position_size / grid_levels
#                 }
#             else:
#                 return {'action': 'HOLD', 'reason': 'En zona neutral del grid'}
                
#         except Exception as e:
#             print(f"Error en grid strategy: {e}")
#             return {'action': 'HOLD', 'reason': f'Error: {str(e)}'}
    
#     async def trailing_stop_strategy(self, config: TradingConfig, current_price: float,
#                                    indicators: Dict) -> Dict:
#         """Estrategia con Trailing Stop"""
#         return {'action': 'HOLD', 'reason': 'Trailing stop strategy not implemented'}
    
#     async def range_bound_strategy(self, config: TradingConfig, current_price: float,
#                                  indicators: Dict) -> Dict:
#         """Estrategia de trading por rango"""
#         if current_price <= config.price_range_min:
#             return {
#                 'action': 'BUY',
#                 'reason': 'Precio en mínimo del rango',
#                 'price': current_price,
#                 'quantity': config.max_position_size
#             }
#         elif current_price >= config.price_range_max:
#             return {
#                 'action': 'SELL',
#                 'reason': 'Precio en máximo del rango', 
#                 'price': current_price,
#                 'quantity': config.max_position_size
#             }
#         else:
#             return {'action': 'HOLD', 'reason': 'Dentro del rango'}
    
#     async def execute_trade(self, config: TradingConfig, decision: Dict, market_data: pd.DataFrame):
#         """Ejecutar trade en Bybit"""
#         try:
#             symbol = config.symbol
#             side = decision['action']
#             quantity = decision.get('quantity', config.max_position_size)
#             price = decision.get('price', float(market_data['close'].iloc[-1]))
            
#             stop_loss = price * (1 - config.stop_loss / 100) if side == 'BUY' else price * (1 + config.stop_loss / 100)
#             take_profit = price * (1 + config.take_profit / 100) if side == 'BUY' else price * (1 - config.take_profit / 100)
            
#             order_result = await bybit_client.place_order(
#                 symbol=symbol,
#                 side=side,
#                 order_type="Limit",
#                 qty=quantity,
#                 price=price,
#                 stop_loss=stop_loss,
#                 take_profit=take_profit
#             )
            
#             if order_result and order_result.get('ret_code') == 0:
#                 trade = Trade(
#                     symbol=symbol,
#                     side=side,
#                     price=price,
#                     quantity=quantity,
#                     strategy=config.strategy_name,
#                     order_id=order_result['result']['order_id']
#                 )
#                 self.db.add(trade)
#                 self.db.commit()
                
#                 await self.create_notification(
#                     f"🎯 {side} ejecutado: {symbol} a {price:.2f}, SL: {stop_loss:.2f}, TP: {take_profit:.2f}"
#                 )
                
#                 print(f"✅ Trade ejecutado: {side} {symbol} a {price}")
            
#         except Exception as e:
#             error_msg = f"❌ Error ejecutando trade: {str(e)}"
#             print(error_msg)
#             await self.create_notification(error_msg)
    
#     async def create_notification(self, message: str):
#         """Crear notificación en la base de datos"""
#         try:
#             notification = Notification(
#                 type="TRADE_EXECUTED",
#                 message=message,
#                 priority="HIGH"
#             )
#             self.db.add(notification)
#             self.db.commit()
#         except Exception as e:
#             print(f"Error creando notificación: {e}")

# trading_bot = None

# async def start_trading_loop():
#     global trading_bot
#     print("🔄 Trading loop listo para iniciar con sesión de BD")

# async def market_analysis_loop():
#     while True:
#         try:
#             if PANDAS_AVAILABLE:
#                 print("📈 Analizando mercado (modo real)...")
#             else:
#                 print("📈 Simulando análisis de mercado...")
#             await asyncio.sleep(300)
#         except Exception as e:
#             print(f"Error en análisis de mercado: {e}")
#             await asyncio.sleep(60)