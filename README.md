# FX Rate Manager

A full-stack application for managing foreign exchange rates and performing currency conversions. Built with FastAPI (backend) and Vue 3 (frontend), demonstrating a clean 3-layer architecture with dependency injection.

## Architecture

The application follows a 3-layer architecture:

- **API Layer** (`app/api/routes/`) - FastAPI routers, HTTP handling only
- **Service Layer** (`app/services/`) - Business logic, no HTTP dependencies
- **Repository Layer** (`app/repositories/`) - Database access via SQLAlchemy

Dependency injection is used throughout to wire components together.

## Tech Stack

### Backend
- Python 3.x
- FastAPI
- SQLAlchemy 2.x (ORM)
- PostgreSQL
- Pydantic (validation)

### Frontend
- Vue 3 (Composition API)
- TypeScript
- Vite
- Axios
- Vue Router

## Project Structure

```
fxrate/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── exchange_rates.py
│   │   │   │   └── conversion.py
│   │   │   └── dependencies.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── db.py
│   │   │   └── models.py
│   │   ├── domain/
│   │   │   └── schemas/
│   │   │       ├── exchange_rate.py
│   │   │       └── conversion.py
│   │   ├── repositories/
│   │   │   └── exchange_rate_repository.py
│   │   ├── services/
│   │   │   ├── exchange_rate_service.py
│   │   │   └── conversion_service.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── seed_data.py
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── views/
│   │   ├── App.vue
│   │   ├── main.ts
│   │   ├── router.ts
│   │   └── style.css
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 12+

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database:**
   ```bash
   createdb fxrate_db
   ```

5. **Configure database connection:**
   ```bash
   cp .env.example .env
   # Edit .env and set your DATABASE_URL
   ```

6. **(Optional) Seed sample data:**
   ```bash
   python seed_data.py
   ```

8. **Start the backend server:**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## API Endpoints

### Exchange Rates

- `GET /exchange-rates` - List all exchange rates (with optional filters)
- `GET /exchange-rates/{id}` - Get a single exchange rate by ID
- `POST /exchange-rates` - Create a new exchange rate
- `PUT /exchange-rates/{id}` - Update an existing exchange rate
- `DELETE /exchange-rates/{id}` - Delete an exchange rate

### Conversion

- `GET /conversion` - Convert currency
  - Query parameters:
    - `amount` (required) - Amount to convert
    - `from_currency` (required) - Source currency code
    - `to_currency` (required) - Target currency code
    - `period` (required) - Period identifier (e.g., "2025-01")

## Example API Calls

### Create an exchange rate:
```bash
curl -X POST "http://localhost:8000/exchange-rates" \
  -H "Content-Type: application/json" \
  -d '{
    "from_currency": "CZK",
    "to_currency": "EUR",
    "period": "2025-01",
    "rate": 0.0405
  }'
```

### List exchange rates:
```bash
curl "http://localhost:8000/exchange-rates?from_currency=CZK&period=2025-01"
```

### Convert currency:
```bash
curl "http://localhost:8000/conversion?amount=1000&from_currency=CZK&to_currency=EUR&period=2025-01"
```

## Docker Setup (Optional)

A `docker-compose.yml` file is provided for easy setup with Docker:

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Backend API (port 8000)
- Frontend (port 5173)

## Features

- **Exchange Rate Management**: Full CRUD operations for exchange rates
- **Currency Conversion**: Convert amounts between currencies using stored rates
- **Filtering**: Filter exchange rates by currency pair and period
- **Validation**: Input validation on both frontend and backend
- **Error Handling**: Clear error messages for API failures
- **Clean Architecture**: Separation of concerns with dependency injection

## Development Notes

- The backend uses FastAPI's dependency injection system to wire services and repositories
- Services contain business logic and validation
- Repositories handle all database operations
- The frontend uses Vue 3 Composition API with TypeScript for type safety
- CORS is configured to allow frontend-backend communication

## License

This is a demo project for interview purposes.

