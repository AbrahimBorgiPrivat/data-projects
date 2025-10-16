from pathlib import Path
CURRENT_DIR = Path(__file__).resolve().parent
RUNTINE_PATH = CURRENT_DIR.parent.parent / "runtime_definitions" 
RES_PATH = Path(__file__).resolve().parents[4] / "res" 