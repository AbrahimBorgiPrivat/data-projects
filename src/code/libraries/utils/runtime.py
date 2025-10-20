import json
from . import env

def load_runtime_vars(JSON_PATH: str):
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    def resolve_env_vars(obj):
        if isinstance(obj, dict):
            return {k: resolve_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [resolve_env_vars(v) for v in obj]
        elif isinstance(obj, str):
            # Try to fetch attribute from env.py dynamically
            if hasattr(env, obj):
                return getattr(env, obj)
            return obj  # keep original if not found
        else:
            return obj
    return resolve_env_vars(config)