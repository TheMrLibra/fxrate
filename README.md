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
│   ├── alembic/
│   ├── alembic.ini
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