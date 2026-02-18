import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / "secrets" / ".env"

load_dotenv(ENV_PATH)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/fraud_dev",
)
# Test database (used by pytest)
DATABASE_URL_TEST = os.getenv(
    "DATABASE_URL_TEST",
    "postgresql+psycopg://postgres:postgres@localhost:5432/fraud_test",
)
