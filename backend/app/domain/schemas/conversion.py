from pydantic import BaseModel, Field
from decimal import Decimal


class ConversionRequest(BaseModel):
    amount: Decimal = Field(..., gt=0, description="Amount to convert (must be positive)")
    from_currency: str = Field(..., min_length=3, max_length=3, description="Source currency code")
    to_currency: str = Field(..., min_length=3, max_length=3, description="Target currency code")
    period: str = Field(..., description="Period identifier (e.g., 2025-01)")


class ConversionResult(BaseModel):
    from_currency: str
    to_currency: str
    period: str
    original_amount: Decimal
    rate: Decimal
    converted_amount: Decimal


