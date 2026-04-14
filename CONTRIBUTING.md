# Contributing to DataQGuard

Thanks for your interest in contributing!

## Development Setup

```bash
# Clone the repository
git clone https://github.com/KaiSong-UK/DataQGuard.git
cd DataQGuard

# Start all services
docker compose up -d

# Access the API docs
open http://localhost:8000/docs

# Access the frontend
open http://localhost:3000
```

## Project Structure

```
backend/
├── main.py              # FastAPI app entry point
├── core/                 # Core modules
│   ├── config.py        # Settings
│   ├── database.py      # Database connection
│   ├── security.py      # Auth utilities
│   └── celery_config.py # Celery config
├── models/               # SQLAlchemy models
├── api/                  # API routes
│   └── routes/
│       ├── auth.py
│       ├── datasources.py
│       ├── rules.py
│       ├── executions.py
│       ├── alerts.py
│       └── dashboard.py
├── services/             # Business logic
│   └── rule_engine.py
└── tasks/                # Celery tasks
    └── rule_executor.py

frontend/
├── src/
│   ├── App.tsx           # Main app component
│   ├── pages/            # Page components
│   │   ├── Dashboard.tsx
│   │   ├── Rules.tsx
│   │   └── ...
│   └── components/       # Reusable components
│       └── Layout/
```

## Adding a New Rule Type

1. Add the rule type to `models/models.py` → `Rule.rule_type`
2. Implement the check method in `services/rule_engine.py`
3. Add the API endpoint in `api/routes/rules.py`

## Pull Request Guidelines

- Follow PEP 8 for Python code
- Follow the existing code style
- Add tests for new features
- Update documentation as needed
