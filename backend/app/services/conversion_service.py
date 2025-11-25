from decimal import Decimal
from fastapi import HTTPException, status

from app.services.exchange_rate_service import ExchangeRateService
from app.domain.schemas.conversion import ConversionResult


class ConversionService:
    def __init__(self, exchange_rate_service: ExchangeRateService):
        self.exchange_rate_service = exchange_rate_service
    
    def convert(
        self,
        amount: Decimal,
        from_currency: str,
        to_currency: str,
        period: str
    ) -> ConversionResult:
        """
        Convert an amount from one currency to another using the exchange rate
        for the specified period.
        """
        # Get the exchange rate
        rate_data = self.exchange_rate_service.get_rate(
            from_currency,
            to_currency,
            period
        )
        
        # Calculate converted amount
        converted_amount = amount * rate_data.rate
        
        return ConversionResult(
            from_currency=from_currency,
            to_currency=to_currency,
            period=period,
            original_amount=amount,
            rate=rate_data.rate,
            converted_amount=converted_amount
        )


