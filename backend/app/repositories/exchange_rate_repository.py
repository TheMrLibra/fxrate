from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from decimal import Decimal

from app.core.models import ExchangeRate
from app.domain.schemas.exchange_rate import ExchangeRateCreate, ExchangeRateUpdate, ExchangeRateFilter


class ExchangeRateRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def list(self, filter_params: Optional[ExchangeRateFilter] = None) -> List[ExchangeRate]:
        """List all exchange rates, optionally filtered."""
        query = self.session.query(ExchangeRate)
        
        if filter_params:
            if filter_params.from_currency:
                query = query.filter(ExchangeRate.from_currency == filter_params.from_currency)
            if filter_params.to_currency:
                query = query.filter(ExchangeRate.to_currency == filter_params.to_currency)
            if filter_params.period:
                query = query.filter(ExchangeRate.period == filter_params.period)
        
        return query.all()
    
    def get_by_id(self, rate_id: int) -> Optional[ExchangeRate]:
        """Get exchange rate by ID."""
        return self.session.query(ExchangeRate).filter(ExchangeRate.id == rate_id).first()
    
    def get_by_key(
        self, 
        from_currency: str, 
        to_currency: str, 
        period: str
    ) -> Optional[ExchangeRate]:
        """Get exchange rate by composite key (from_currency, to_currency, period)."""
        return self.session.query(ExchangeRate).filter(
            and_(
                ExchangeRate.from_currency == from_currency,
                ExchangeRate.to_currency == to_currency,
                ExchangeRate.period == period
            )
        ).first()
    
    def create(self, data: ExchangeRateCreate) -> ExchangeRate:
        """Create a new exchange rate."""
        rate = ExchangeRate(
            from_currency=data.from_currency,
            to_currency=data.to_currency,
            period=data.period,
            rate=data.rate
        )
        self.session.add(rate)
        self.session.commit()
        self.session.refresh(rate)
        return rate
    
    def update(self, rate: ExchangeRate, data: ExchangeRateUpdate) -> ExchangeRate:
        """Update an existing exchange rate."""
        if data.from_currency is not None:
            rate.from_currency = data.from_currency
        if data.to_currency is not None:
            rate.to_currency = data.to_currency
        if data.period is not None:
            rate.period = data.period
        if data.rate is not None:
            rate.rate = data.rate
        
        self.session.commit()
        self.session.refresh(rate)
        return rate
    
    def delete(self, rate: ExchangeRate) -> None:
        """Delete an exchange rate."""
        self.session.delete(rate)
        self.session.commit()

