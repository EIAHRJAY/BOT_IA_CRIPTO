from sqlalchemy.orm import Session
from models import TradingConfig, Trade, MarketData, Notification, AIDecision
from schemas import TradingConfigCreate, TradeCreate, MarketDataCreate, NotificationCreate, AIDecisionCreate

# TradingConfig CRUD
def get_trading_config(db: Session, config_id: int):
    return db.query(TradingConfig).filter(TradingConfig.id == config_id).first()

def get_trading_configs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TradingConfig).offset(skip).limit(limit).all()

def get_active_strategies(db: Session):
    return db.query(TradingConfig).filter(TradingConfig.is_active == True).all()

def create_trading_config(db: Session, config: TradingConfigCreate):
    db_config = TradingConfig(**config.dict())
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

# Trade CRUD
def get_trades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Trade).offset(skip).limit(limit).all()

def create_trade(db: Session, trade: TradeCreate):
    db_trade = Trade(**trade.dict())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

# MarketData CRUD
def create_market_data(db: Session, market_data: MarketDataCreate):
    db_market_data = MarketData(**market_data.dict())
    db.add(db_market_data)
    db.commit()
    db.refresh(db_market_data)
    return db_market_data

# Notification CRUD
def get_pending_notifications(db: Session):
    return db.query(Notification).filter(Notification.sent == False).all()

def create_notification(db: Session, notification: NotificationCreate):
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def mark_notification_sent(db: Session, notification_id: int):
    db_notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if db_notification:
        db_notification.sent = True
        db.commit()
        db.refresh(db_notification)
    return db_notification

# AIDecision CRUD
def create_ai_decision(db: Session, ai_decision: AIDecisionCreate):
    db_ai_decision = AIDecision(**ai_decision.dict())
    db.add(db_ai_decision)
    db.commit()
    db.refresh(db_ai_decision)
    return db_ai_decision

def get_ai_decisions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AIDecision).offset(skip).limit(limit).all()