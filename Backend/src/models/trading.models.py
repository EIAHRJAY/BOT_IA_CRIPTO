from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from datetime import datetime
from database import Base

class TradingConfig(Base):
    __tablename__ = "trading_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    strategy_name = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Estrategia parameters
    price_range_min = Column(Float)
    price_range_max = Column(Float)
    grid_levels = Column(Integer)
    trailing_stop = Column(Float)
    trailing_up = Column(Boolean, default=False)
    entry_price = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)
    
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
    status = Column(String, default="OPEN")  # OPEN/CLOSED/CANCELLED

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

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # STRATEGY_CHANGE, DAILY_UPDATE, ALERT
    message = Column(Text)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AIDecision(Base):
    __tablename__ = "ai_decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    decision = Column(String)  # BUY/SELL/HOLD
    confidence = Column(Float)
    reasoning = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    executed = Column(Boolean, default=False)