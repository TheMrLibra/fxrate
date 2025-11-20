from decimal import Decimal
from fastapi import APIRouter, Depends, Query

from app.services.conversion_service import ConversionService
from app.domain.schemas.conversion import ConversionResult
from app.api.dependencies import get_conversion_service
from app.core.security import get_current_active_user
from app.core.models import User

router = APIRouter(prefix="/conversion", tags=["conversion"])


@router.get("", response_model=ConversionResult)
def convert_currency(
    amount: Decimal = Query(..., description="Amount to convert", gt=0),
    from_currency: str = Query(..., description="Source currency code", min_length=3, max_length=3),
    to_currency: str = Query(..., description="Target currency code", min_length=3, max_length=3),
    period: str = Query(..., description="Period identifier (e.g., 2025-01)"),
    service: ConversionService = Depends(get_conversion_service),
    current_user: User = Depends(get_current_active_user),
):
    """
    Convert an amount from one currency to another using the exchange rate
    for the specified period.
    """
    return service.convert(amount, from_currency, to_currency, period)

