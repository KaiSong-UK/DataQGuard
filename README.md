# DataQGuard

Open-source data quality monitoring platform with real-time dashboards, rule engine & smart alerting.

## Quick Start

```bash
git clone https://github.com/KaiSong-UK/DataQGuard.git
cd DataQGuard
docker compose up --build
```

Open http://localhost:8000

> Default credentials: `admin@dataqguard.com` / `admin123`

## Project Structure

```
DataQGuard/
├── backend/          FastAPI + SQLAlchemy (asyncpg)
├── frontend/         React 18 + TypeScript + Ant Design + ECharts
├── docker-compose.yml
└── README.md
```

## Features

- ✅ Rule Engine (completeness, accuracy, uniqueness, timeliness)
- ✅ Real-time Dashboard with charts
- ✅ Multi-channel Alerting (email, Slack, webhook)
- ✅ Cron-based scheduling via Celery Beat
- ✅ PostgreSQL & MySQL connectors
- ✅ ClickHouse metrics store
- 🚧 AI anomaly detection (coming)

## Architecture

```
Browser → FastAPI (port 8000) → PostgreSQL (data)
                          → Redis (Celery)
                          → ClickHouse (metrics)
```

## Development (without Docker)

```bash
# Backend
cd backend
cp .env.example .env
pip install -r requirements.txt
python seed_data.py   # seed demo data
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## License

MIT
