from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import exchange_rates, conversion, auth

app = FastAPI(
    title="FX Rate Manager",
    description="Foreign Exchange Rate Management and Conversion API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://192.168.1.204:5173",
        "https://fx.adamlibra.cz",
        "http://fx.adamlibra.cz",
    ],
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

