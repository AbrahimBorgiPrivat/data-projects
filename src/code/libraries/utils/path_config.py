from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
RUNTIME_PATH = CURRENT_DIR.parent.parent / "runtime_definitions"

DOCKER_RES_PATH = Path("/app/res")

if DOCKER_RES_PATH.exists():
    RES_PATH = DOCKER_RES_PATH
else:
    LOCAL_RES_PATH = Path(__file__).resolve().parents[4] / "res"
    RES_PATH = LOCAL_RES_PATH

print(f"[path_config] Using RES_PATH={RES_PATH}")