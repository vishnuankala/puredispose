from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.database import Base, engine
from app.routers import orders, products, enquiries

# Create tables if they don't exist yet (fine for dev; use Alembic migrations in prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PureDispose API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- API routes ----
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(enquiries.router)

# ---- Frontend: multi-page site, each page its own route ----
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"

app.mount("/styles", StaticFiles(directory=FRONTEND_DIR / "styles"), name="styles")
app.mount("/scripts", StaticFiles(directory=FRONTEND_DIR / "scripts"), name="scripts")


@app.get("/")
def serve_home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/products")
@app.get("/products.html")
def serve_products():
    return FileResponse(FRONTEND_DIR / "products.html")


@app.get("/pricing")
@app.get("/pricing.html")
def serve_pricing():
    return FileResponse(FRONTEND_DIR / "pricing.html")
