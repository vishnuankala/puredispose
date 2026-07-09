import os
from pathlib import Path

# Load .env file if python-dotenv is installed and a .env exists at project root
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")
except ImportError:
    pass


class Settings:
    # PostgreSQL connection. Override these in your .env file.
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "puredispose")

    @property
    def database_url(self) -> str:
        # Hosting platforms (Railway, Render, Heroku) inject a single
        # DATABASE_URL env var instead of separate DB_* vars. Prefer it
        # when present, and fall back to the individual vars for local dev.
        url = os.getenv("DATABASE_URL")
        if url:
            # Railway/Heroku sometimes give "postgres://" - normalize and use
            # pg8000 (pure Python, no system libpq dependency needed)
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql+pg8000://", 1)
            elif url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+pg8000://", 1)
            return url

        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # CORS - add your deployed frontend origin(s) here in production
    ALLOWED_ORIGINS: list[str] = os.getenv(
        "ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000"
    ).split(",")


settings = Settings()
