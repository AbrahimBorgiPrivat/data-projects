import os
import importlib
from pathlib import Path
from libraries.utils import runtime

def run_runner(module_path: str, runtime_json_path: Path):
    print(f"\n[main] 🚀 Running {module_path} using {runtime_json_path}")
    module = importlib.import_module(module_path)
    if not hasattr(module, "main"):
        raise AttributeError(f"Module {module_path} has no 'main' function")
    upsert_runtime_vars = runtime.load_runtime_vars(JSON_PATH=runtime_json_path)
    print(upsert_runtime_vars)
    module.main(upsert_runtime_vars)
    print(f"[main] ✅ Completed: {runtime_json_path.name}")

if __name__ == "__main__":
    CURRENT_DIR = Path(__file__).resolve().parent
    RUNTIME_BASE = CURRENT_DIR.parent / "runtime_definitions" / "tv1" / "simulations" / "runtime"
    runner_module = os.getenv("RUNNER_MODULE", "libraries.runners.runners")
    runtime_files_env = os.getenv("RUNTIME_FILES", "passports.json")
    runtime_files = [f.strip() for f in runtime_files_env.split(",") if f.strip()]
    for filename in runtime_files:
        runtime_json = RUNTIME_BASE / filename
        if not runtime_json.exists():
            print(f"[main] ⚠️ Warning: {runtime_json} not found — skipping.")
            continue
        run_runner(runner_module, runtime_json)
    print("\n[main] ✅ All runtime files processed successfully.")