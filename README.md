# 🎲 Farkle Backend

A FastAPI + SQLAlchemy backend service for the **Farkle (Mobile)** Unity game.\
Handles persistent player profiles, match history, statistics, and leaderboards, with a simple REST API ready for integration with any client.

---

## 📖 Overview

This backend is designed to:

- Store player profiles linked to a user (Google Play ID or anonymous UUID)
- Track completed matches and detailed results for each player
- Provide aggregated player statistics
- Serve global leaderboards sorted by multiple metrics

It’s built as a **portfolio-quality** example of a modular, scalable backend service.

---

## 🛠️ Tech Stack

- [**FastAPI**](https://fastapi.tiangolo.com/) — Python web framework with automatic interactive docs
- [**SQLAlchemy**](https://www.sqlalchemy.org/) — ORM for database models and queries
- **SQLite** (local dev) / **PostgreSQL** (production) — relational data storage
- **Pydantic** — request/response schema validation
- **Uvicorn** — ASGI server for FastAPI apps

---

## 📂 Project Structure

```
backend/
│
├── __init__.py            # Package marker + docs
├── main.py                # FastAPI entry point and routes
├── database.py            # Engine, session, Base model, get_db()
├── models.py              # SQLAlchemy ORM models
├── schemas.py             # Pydantic request/response classes
├── crud.py                # Database helper functions
│
├── tests/                 # Unit/integration tests
│   └── __init__.py
│   └── test_endpoints.py
│
└── scripts/               # Utility scripts (seeders, migrations, etc.)
    └── __init__.py
    └── seed_dev_data.py  # Populate local DB with sample data
```

---

## 🚀 Getting Started

### 1. Clone and Install

```bash
git clone https://github.com/b-hopper/farkle-server.git
cd farkle-backend
```

**For production:**
```bash
pip install -r requirements.txt
```

**For local development & testing:**
```bash
pip install -r requirements-dev.txt
```

It’s recommended to use a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

---

---

### 2. Configure Database

By default, the backend uses a local SQLite database (`farkle.db`).\
To change, set the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL="sqlite:///./farkle.db"  # macOS/Linux
set DATABASE_URL=sqlite:///./farkle.db       # Windows cmd
```

Example for PostgreSQL:

```bash
export DATABASE_URL="postgresql://user:pass@localhost:5432/farkle"
```

---

### 3. Run the Server

```bash
uvicorn backend.main:app --reload
```

- API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Interactive Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔌 API Endpoints

### Create Player

`POST /create-player`\
Creates a new player profile under a user account.

### Submit Game Result

`POST /game-result`\
Stores a completed match with results for each player.

### Get Player Stats

`GET /player-stats?player_id={id}`\
Returns aggregated statistics for a player.

### Get Leaderboard

`GET /leaderboard?sort=avg_score|wins|total_points`\
Returns leaderboard entries sorted by the chosen metric.

### List User’s Players

`GET /user-players?user_id={id}`\
Lists all player profiles associated with a user.

---

## 📈 Development Utilities

- **Seeding Data** — Populate the local database with sample users, players, and matches for development/testing.

  ```bash
  # From the project root
  python -m backend.scripts.seed_dev_data
  ```

- **Tests** — Run unit tests to ensure everything works as expected.

  ```bash
  # From the project root
  pytest backend/tests
  ```
  Or use the built-in test command:

  ```bash
  python -m unittest discover backend/tests
  ```
---

## 🌐 Deployment

Can be deployed to:

- [Render](https://render.com/) or [Railway](https://railway.app/) for simple PaaS hosting
- [Google Cloud Run](https://cloud.google.com/run) if integrating with Google Play auth
- [Supabase](https://supabase.com/), [Neon.tech](https://neon.tech/), or [ElephantSQL](https://www.elephantsql.com/) for managed PostgreSQL

---

## 📜 License

This backend is open-source and available for educational or portfolio purposes.\
Attribution is appreciated.

---

Made with ❤️ for the **Farkle (Mobile)** project.

