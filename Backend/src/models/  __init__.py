from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from datetime import datetime
from database import Base

class TradingConfig(Base):
    __tablename__ = "trading_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    strategy_name = Column(String, default="GRID")
    is_active = Column(Boolean, default=True)
    
    # Parámetros de estrategia
    price_range_min = Column(Float)
    price_range_max = Column(Float)
    grid_levels = Column(Integer, default=10)
    trailing_stop = Column(Float, default=2.0)
    trailing_up = Column(Boolean, default=False)
    entry_price = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)
    
    # Configuración de riesgo
    max_position_size = Column(Float, default=100.0)
    leverage = Column(Integer, default=1)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    side = Column(String)  # BUY/SELL
    price = Column(Float)
    quantity = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    strategy = Column(String)
    pnl = Column(Float, default=0.0)
    status = Column(String, default="OPEN")
    order_id = Column(String, unique=True)

class MarketData(Base):
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    interval = Column(String, default="1h")

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # TRADE_SIGNAL, STRATEGY_CHANGE, DAILY_REPORT, ALERT
    message = Column(Text)
    priority = Column(String, default="MEDIUM")  # LOW, MEDIUM, HIGH, URGENT
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AIDecision(Base):
    __tablename__ = "ai_decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    decision = Column(String)  # BUY/SELL/HOLD
    confidence = Column(Float)
    reasoning = Column(Text)
    indicators = Column(JSON)  # Datos técnicos usados para la decisión
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    executed = Column(Boolean, default=False)