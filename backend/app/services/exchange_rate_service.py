from typing import List, Optional
from fastapi import HTTPException, status

from app.repositories.exchange_rate_repository import ExchangeRateRepository
from app.domain.schemas.exchange_rate import (
    ExchangeRateCreate,
    ExchangeRateUpdate,
    ExchangeRateRead,
    ExchangeRateFilter
)


class ExchangeRateService:
    def __init__(self, repository: ExchangeRateRepository):
        self.repository = repository
    
    def get_rates(self, filter_params: Optional[ExchangeRateFilter] = None) -> List[ExchangeRateRead]:
        """Get all exchange rates, optionally filtered."""
        rates = self.repository.list(filter_params)
        return [ExchangeRateRead.model_validate(rate) for rate in rates]
    
    def get_rate_by_id(self, rate_id: int) -> ExchangeRateRead:
        """Get exchange rate by ID."""
        rate = self.repository.get_by_id(rate_id)
        if not rate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exchange rate with id {rate_id} not found"
            )
        return ExchangeRateRead.model_validate(rate)
    
    def create_rate(self, data: ExchangeRateCreate) -> ExchangeRateRead:
        """Create a new exchange rate."""
        # Check if rate already exists for this combination
        existing = self.repository.get_by_key(
            data.from_currency,
            data.to_currency,
            data.period
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Exchange rate for {data.from_currency}->{data.to_currency} "
                       f"for period {data.period} already exists"
            )
        
        # Validate rate is positive (already validated by Pydantic, but double-check)
        if data.rate <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Exchange rate must be positive"
            )
        
        rate = self.repository.create(data)
        return ExchangeRateRead.model_validate(rate)
    
    def update_rate(self, rate_id: int, data: ExchangeRateUpdate) -> ExchangeRateRead:
        """Update an existing exchange rate."""
        rate = self.repository.get_by_id(rate_id)
        if not rate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exchange rate with id {rate_id} not found"
            )
        
        # If updating to a new combination, check if it already exists
        new_from = data.from_currency if data.from_currency is not None else rate.from_currency
        new_to = data.to_currency if data.to_currency is not None else rate.to_currency
        new_period = data.period if data.period is not None else rate.period
        
        if (new_from != rate.from_currency or 
            new_to != rate.to_currency or 
            new_period != rate.period):
            existing = self.repository.get_by_key(new_from, new_to, new_period)
            if existing and existing.id != rate_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Exchange rate for {new_from}->{new_to} "
                           f"for period {new_period} already exists"
                )
        
        # Validate rate if provided
        if data.rate is not None and data.rate <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Exchange rate must be positive"
            )
        
        updated_rate = self.repository.update(rate, data)
        return ExchangeRateRead.model_validate(updated_rate)
    
    def delete_rate(self, rate_id: int) -> None:
        """Delete an exchange rate."""
        rate = self.repository.get_by_id(rate_id)
        if not rate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exchange rate with id {rate_id} not found"
            )
        self.repository.delete(rate)
    
    def get_rate(
        self, 
        from_currency: str, 
        to_currency: str, 
        period: str
    ) -> ExchangeRateRead:
        """Get exchange rate by composite key."""
        rate = self.repository.get_by_key(from_currency, to_currency, period)
        if not rate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exchange rate for {from_currency}->{to_currency} "
                       f"for period {period} not found"
            )
        return ExchangeRateRead.model_validate(rate)


