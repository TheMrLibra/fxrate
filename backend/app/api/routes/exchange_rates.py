from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from app.services.exchange_rate_service import ExchangeRateService
from app.domain.schemas.exchange_rate import (
    ExchangeRateCreate,
    ExchangeRateUpdate,
    ExchangeRateRead,
    ExchangeRateFilter
)
from app.api.dependencies import get_exchange_rate_service
from app.core.security import get_current_active_user
from app.core.models import User

router = APIRouter(prefix="/exchange-rates", tags=["exchange-rates"])


@router.get("", response_model=list[ExchangeRateRead])
def list_exchange_rates(
    from_currency: Optional[str] = Query(None, description="Filter by source currency"),
    to_currency: Optional[str] = Query(None, description="Filter by target currency"),
    period: Optional[str] = Query(None, description="Filter by period"),
    service: ExchangeRateService = Depends(get_exchange_rate_service),
    current_user: User = Depends(get_current_active_user),
):
    """List all exchange rates, optionally filtered."""
    filter_params = ExchangeRateFilter(
        from_currency=from_currency,
        to_currency=to_currency,
        period=period
    )
    return service.get_rates(filter_params)


@router.post("", response_model=ExchangeRateRead, status_code=status.HTTP_201_CREATED)
def create_exchange_rate(
    data: ExchangeRateCreate,
    service: ExchangeRateService = Depends(get_exchange_rate_service),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new exchange rate."""
    return service.create_rate(data)


@router.get("/{rate_id}", response_model=ExchangeRateRead)
def get_exchange_rate(
    rate_id: int,
    service: ExchangeRateService = Depends(get_exchange_rate_service),
    current_user: User = Depends(get_current_active_user),
):
    """Get a single exchange rate by ID."""
    return service.get_rate_by_id(rate_id)


@router.put("/{rate_id}", response_model=ExchangeRateRead)
def update_exchange_rate(
    rate_id: int,
    data: ExchangeRateUpdate,
    service: ExchangeRateService = Depends(get_exchange_rate_service),
    current_user: User = Depends(get_current_active_user),
):
    """Update an existing exchange rate."""
    return service.update_rate(rate_id, data)


@router.delete("/{rate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exchange_rate(
    rate_id: int,
    service: ExchangeRateService = Depends(get_exchange_rate_service),
    current_user: User = Depends(get_current_active_user),
):
    """Delete an exchange rate."""
    service.delete_rate(rate_id)
    return None

