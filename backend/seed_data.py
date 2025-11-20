"""
Seed script to populate the database with sample exchange rates.
Run this after setting up the database and running migrations.
"""
from decimal import Decimal
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.repositories.exchange_rate_repository import ExchangeRateRepository
from app.domain.schemas.exchange_rate import ExchangeRateCreate


def seed_exchange_rates():
    """Seed the database with sample exchange rates."""
    db: Session = SessionLocal()
    try:
        repo = ExchangeRateRepository(db)
        
        # Sample exchange rates
        sample_rates = [
            ExchangeRateCreate(
                from_currency="CZK",
                to_currency="EUR",
                period="2025-01",
                rate=Decimal("0.0405")
            ),
            ExchangeRateCreate(
                from_currency="CZK",
                to_currency="USD",
                period="2025-01",
                rate=Decimal("0.0442")
            ),
            ExchangeRateCreate(
                from_currency="EUR",
                to_currency="USD",
                period="2025-01",
                rate=Decimal("1.0912")
            ),
            ExchangeRateCreate(
                from_currency="USD",
                to_currency="EUR",
                period="2025-01",
                rate=Decimal("0.9164")
            ),
            ExchangeRateCreate(
                from_currency="GBP",
                to_currency="EUR",
                period="2025-01",
                rate=Decimal("1.1680")
            ),
            ExchangeRateCreate(
                from_currency="EUR",
                to_currency="GBP",
                period="2025-01",
                rate=Decimal("0.8562")
            ),
        ]
        
        for rate_data in sample_rates:
            # Check if rate already exists
            existing = repo.get_by_key(
                rate_data.from_currency,
                rate_data.to_currency,
                rate_data.period
            )
            if not existing:
                repo.create(rate_data)
                print(f"Created rate: {rate_data.from_currency} -> {rate_data.to_currency} "
                      f"({rate_data.period}): {rate_data.rate}")
            else:
                print(f"Rate already exists: {rate_data.from_currency} -> {rate_data.to_currency} "
                      f"({rate_data.period})")
        
        print("\nSeed data populated successfully!")
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_exchange_rates()

