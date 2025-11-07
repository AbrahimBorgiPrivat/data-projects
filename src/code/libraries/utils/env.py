from dotenv import load_dotenv
from pathlib import Path
import os

IN_DOCKER = Path("/.dockerenv").exists()
if IN_DOCKER:
    print("[env.py] Docker environment detected — skipping .env.local load")
else:
    env_local = Path(__file__).resolve().parent / ".env.local"
    if env_local.exists():
        print(f"[env.py] Loading local environment from {env_local}")
        load_dotenv(dotenv_path=env_local, override=True, verbose=True)
    else:
        print("[env.py] No local .env.local found")

POSTGRES_DB = os.getenv("POSTGRES_DB")
TV_OME_DB = os.getenv("TV_OME_DB")
CPH_AIRPORT_DB = os.getenv("CPH_AIRPORT_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_TYPE = os.getenv("DB_TYPE")

GAMMA_HOST = os.getenv("GAMMA_HOST")
GAMMA_DB = os.getenv("GAMMA_DB")
GAMMA_PORT = os.getenv("GAMMA_PORT")
GAMMA_USERNAME = os.getenv("GAMMA_USERNAME")
GAMMA_PASSWORD = os.getenv("GAMMA_PASSWORD")
GAMMA_DB_TYPE = os.getenv("GAMMA_DB_TYPE")

API_MARKET_KEY=os.getenv("API_MARKET_KEY")