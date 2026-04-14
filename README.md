# DataQGuard

Open-source data quality monitoring platform with real-time dashboards, rule engine & smart alerting.

## Quick Start

```bash
git clone https://github.com/KaiSong-UK/DataQGuard.git
cd DataQGuard
docker compose up -d
```

Open http://localhost:3000

Default login: admin / admin123

## Project Structure

```
DataQGuard/
├── backend/          FastAPI + PostgreSQL + ClickHouse
├── frontend/         React + TypeScript + Ant Design
├── docker-compose.yml
└── README.md
```

## Features

- ✅ Rule Engine (completeness, accuracy, consistency, timeliness)
- ✅ Real-time Dashboard
- ✅ Multi-channel Alerting
- ✅ PostgreSQL & MySQL connectors
- 🚧 AI anomaly detection (coming)

## License

MIT
