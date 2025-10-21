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
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_TYPE = os.getenv("DB_TYPE")

print(f"[env.py] DB connection → {POSTGRES_USERNAME}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
