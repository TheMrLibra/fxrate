from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional


class ExchangeRateBase(BaseModel):
    from_currency: str = Field(..., min_length=3, max_length=3, description="Source currency code (CZK)")
    to_currency: str = Field(..., min_length=3, max_length=3, description="Target currency code (EUR)")
    period: str = Field(..., description="Period identifier (2025-01)")
    rate: Decimal = Field(..., gt=0, description="Exchange rate (must be positive)")


class ExchangeRateCreate(ExchangeRateBase):
    pass


class ExchangeRateUpdate(BaseModel):
    from_currency: Optional[str] = Field(None, min_length=3, max_length=3)
    to_currency: Optional[str] = Field(None, min_length=3, max_length=3)
    period: Optional[str] = None
    rate: Optional[Decimal] = Field(None, gt=0)


class ExchangeRateRead(ExchangeRateBase):
    id: int
    
    class Config:
        from_attributes = True


class ExchangeRateFilter(BaseModel):
    from_currency: Optional[str] = None
    to_currency: Optional[str] = None
    period: Optional[str] = None

