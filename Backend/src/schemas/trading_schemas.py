from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TradingConfigBase(BaseModel):
    symbol: str
    strategy_name: str
    is_active: bool = True
    price_range_min: float
    price_range_max: float
    grid_levels: int
    trailing_stop: float
    trailing_up: bool = False
    entry_price: float
    stop_loss: float
    take_profit: float

class TradingConfigCreate(TradingConfigBase):
    pass

class TradingConfig(TradingConfigBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class TradeBase(BaseModel):
    symbol: str
    side: str
    price: float
    quantity: float
    strategy: str
    pnl: Optional[float] = 0.0
    status: str = "OPEN"

class TradeCreate(TradeBase):
    pass

class Trade(TradeBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class MarketDataBase(BaseModel):
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float

class MarketDataCreate(MarketDataBase):
    pass

class MarketData(MarketDataBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class NotificationBase(BaseModel):
    type: str
    message: str

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    sent: bool
    created_at: datetime

    class Config:
        orm_mode = True

class AIDecisionBase(BaseModel):
    symbol: str
    decision: str
    confidence: float
    reasoning: str

class AIDecisionCreate(AIDecisionBase):
    pass

class AIDecision(AIDecisionBase):
    id: int
    timestamp: datetime
    executed: bool

    class Config:
        orm_mode = True