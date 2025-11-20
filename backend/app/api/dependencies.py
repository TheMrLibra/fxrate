from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db import get_session
from app.repositories.exchange_rate_repository import ExchangeRateRepository
from app.repositories.user_repository import UserRepository
from app.services.exchange_rate_service import ExchangeRateService
from app.services.conversion_service import ConversionService
from app.services.auth_service import AuthService


def get_exchange_rate_repository(
    session: Session = Depends(get_session),
) -> ExchangeRateRepository:
    """Dependency that provides ExchangeRateRepository."""
    return ExchangeRateRepository(session)


def get_exchange_rate_service(
    repository: ExchangeRateRepository = Depends(get_exchange_rate_repository),
) -> ExchangeRateService:
    """Dependency that provides ExchangeRateService."""
    return ExchangeRateService(repository)


def get_conversion_service(
    exchange_rate_service: ExchangeRateService = Depends(get_exchange_rate_service),
) -> ConversionService:
    """Dependency that provides ConversionService."""
    return ConversionService(exchange_rate_service)


def get_user_repository(
    session: Session = Depends(get_session),
) -> UserRepository:
    """Dependency that provides UserRepository."""
    return UserRepository(session)


def get_auth_service(
    repository: UserRepository = Depends(get_user_repository),
    session: Session = Depends(get_session),
) -> AuthService:
    """Dependency that provides AuthService."""
    return AuthService(repository, session)

