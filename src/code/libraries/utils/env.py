import os
from pathlib import Path
from dotenv import load_dotenv

def find_service_root() -> Path | None:
    p = Path(__file__).resolve()
    while p.name:
        if p.name == "service":
            return p
        if p.parent == p:
            break
        p = p.parent
    return None

SERVICE_ROOT = find_service_root()
IN_SERVICE_MODE = SERVICE_ROOT is not None
if IN_SERVICE_MODE:
    ETL_DIR = SERVICE_ROOT / "gamma" / "etl"
    SERVICE_NAME = os.getenv("SERVICE_NAME")
    if not SERVICE_NAME:
        cwd = Path.cwd()
        for part in cwd.parts[::-1]:
            if part.startswith("service_"):
                SERVICE_NAME = part
                break
    if not SERVICE_NAME:
        raise EnvironmentError("SERVICE_NAME not found or could not be inferred in service mode.")
    ENV_MODE = os.getenv("ENV_MODE", "docker").lower()
    print(f"[env.py] Service mode detected for: {SERVICE_NAME} ({ENV_MODE})")
    env_candidates = [
        ETL_DIR / SERVICE_NAME / f".env.{ENV_MODE}",
        ETL_DIR / SERVICE_NAME / ".env",
    ]
    env_file = next((p for p in env_candidates if p.exists()), None)
else:
    print("[env.py] Local mode detected (no service folder found).")
    env_local = Path(__file__).resolve().parent.parent / ".env.local"
    env_default = Path(__file__).resolve().parent.parent / ".env"
    env_file = env_local if env_local.exists() else (env_default if env_default.exists() else None)

if env_file and env_file.exists():
    print(f"[env.py] Loading environment from {env_file}")
    load_dotenv(dotenv_path=env_file, override=True, verbose=True)
else:
    print("[env.py] No .env file found; falling back to system environment.")
    load_dotenv(override=True, verbose=True)

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_TYPE = os.getenv("DB_TYPE")

GAMMA_DB = os.getenv("GAMMA_DB")
GAMMA_HOST = os.getenv("GAMMA_HOST")
GAMMA_PORT = os.getenv("GAMMA_PORT")
GAMMA_USERNAME = os.getenv("GAMMA_USERNAME")
GAMMA_PASSWORD = os.getenv("GAMMA_PASSWORD")
GAMMA_DB_TYPE = os.getenv("GAMMA_DB_TYPE")

required_vars = [
    "POSTGRES_DB", "POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_USERNAME",
    "POSTGRES_PASSWORD", "DB_TYPE", "GAMMA_DB", "GAMMA_HOST",
    "GAMMA_PORT", "GAMMA_USERNAME", "GAMMA_PASSWORD", "GAMMA_DB_TYPE"
]

missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    print(f"[env.py] ⚠️ Missing variables: {missing}")
else:
    print("[env.py] Environment variables loaded successfully ✅")

