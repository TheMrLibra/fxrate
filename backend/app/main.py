from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import exchange_rates, conversion, auth

app = FastAPI(
    title="FX Rate Manager",
    description="Foreign Exchange Rate Management and Conversion API",
    version="1.0.0"
)

# Configure CORS
import os

# Get allowed origins from environment or use defaults
allowed_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:3000,https://fx.adamlibra.cz,http://fx.adamlibra.cz"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(exchange_rates.router)
app.include_router(conversion.router)


@app.get("/")
def root():
    return {
        "message": "FX Rate Manager API",
        "docs": "/docs",
        "version": "1.0.0"
    }

