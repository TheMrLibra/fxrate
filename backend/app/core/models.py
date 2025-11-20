from sqlalchemy import Column, Integer, String, Numeric, UniqueConstraint, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    
    id = Column(Integer, primary_key=True, index=True)
    from_currency = Column(String(3), nullable=False, index=True)
    to_currency = Column(String(3), nullable=False, index=True)
    period = Column(String(10), nullable=False, index=True)
    rate = Column(Numeric(18, 8), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('from_currency', 'to_currency', 'period', name='uq_exchange_rate'),
    )

