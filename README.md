# PureDispose

Disposable tableware site — multi-page frontend (HTML/CSS/JS) backed by a Python FastAPI + PostgreSQL backend.

## Project structure

```
puredispose/
├── frontend/
│   ├── index.html          # Home page (hero, why-us, contact form)
│   ├── products.html       # Product catalog page
│   ├── pricing.html        # Pricing table page
│   ├── styles/
│   │   └── main.css        # All site styling
│   └── scripts/
│       └── main.js         # UI behavior + calls to the backend API
├── backend/
│   ├── app/
│   │   ├── main.py         # FastAPI entrypoint, serves pages + mounts API
│   │   ├── config.py       # Reads settings from .env
│   │   ├── database.py     # SQLAlchemy engine/session
│   │   ├── schemas.py      # Pydantic request/response models
│   │   ├── models/         # SQLAlchemy tables (Order, Product, Enquiry)
│   │   ├── routers/        # API endpoints (orders, products, enquiries)
│   │   └── services/       # Business logic (this is where AI features plug in)
│   ├── alembic/             # Database migrations
│   ├── seed.py              # Populates product catalog table
│   ├── requirements.txt
│   └── alembic.ini
├── .env.example
├── .gitignore
└── README.md
```

## Setup

### 1. PostgreSQL

Create a local database:

```bash
createdb puredispose
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp ../.env.example ../.env       # then edit ../.env with your DB password
```

### 3. Run migrations (creates tables)

```bash
alembic revision --autogenerate -m "initial tables"
alembic upgrade head
```

(Alternatively, `main.py` also auto-creates tables on startup for quick local dev.)

### 4. Seed sample product data (optional)

```bash
python seed.py
```

### 5. Start the server

```bash
uvicorn app.main:app --reload
```

Visit:
- **Site**: http://localhost:8000/
- **Products page**: http://localhost:8000/products
- **Pricing page**: http://localhost:8000/pricing
- **API docs (auto-generated)**: http://localhost:8000/docs

## How pages connect

FastAPI serves each HTML page as its own route (`/`, `/products`, `/pricing`),
so navigating between them is a normal page load — no JS router needed.
`styles/` and `scripts/` are mounted as static folders so every page can share
the same CSS and JS files.

## API endpoints

| Method | Path             | Purpose                                   |
|--------|------------------|--------------------------------------------|
| POST   | `/api/orders`    | Save a "Get a Quote" phone number request  |
| GET    | `/api/orders`    | List recent quote requests (admin)         |
| GET    | `/api/products`  | List catalog products, optional `?category=` |
| POST   | `/api/enquiries` | Log a product "+" click                   |

## Deploying to Railway (production)

1. Push this project to a GitHub repo.
2. On [railway.app](https://railway.app), create a new project → "Deploy from GitHub repo" → select it.
3. Click "+ New" → "Database" → "PostgreSQL" to add a managed Postgres instance in the same project. Railway automatically injects a `DATABASE_URL` variable that the app already knows how to use (see `config.py`).
4. On your web service, go to Variables and add:
   - `ALLOWED_ORIGINS` = your Railway-provided domain (e.g. `https://puredispose-production.up.railway.app`)
5. Railway detects the `Procfile` and `runtime.txt` automatically and deploys.
6. Once deployed, run the one-time table creation/seed by opening the Railway service's shell (or a local `psql` connection using the DB credentials Railway shows you) and running `python backend/seed.py`.
7. Visit the public URL Railway gives you — that's your live site, reachable from any device, anywhere.

## Where to add AI later

`backend/app/services/order_service.py` has a comment marking exactly where an
AI/bot call (e.g. auto-drafting a follow-up message, or a chat assistant) would
plug in — the service layer already has full business context before a
response is returned, which is the cleanest place for that kind of call.
