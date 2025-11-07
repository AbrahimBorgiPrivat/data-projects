import importlib.util
import hashlib
import os

def load_handler(handler_path: str, func_name: str, base_dir: str = None):
    if not handler_path:
        return None
    if base_dir is None:
        base_dir = os.path.join(os.path.dirname(__file__), "../../runtime_definitions")
    abs_path = os.path.abspath(os.path.join(base_dir, handler_path))
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Handler file not found: {abs_path}")
    module_name = os.path.splitext(os.path.basename(abs_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, abs_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, func_name):
        raise AttributeError(f"No function '{func_name}' found in {abs_path}")
    return getattr(module, func_name)

def _generate_hash_id(record: dict, key_fields: list[str]) -> str:
    key_parts = []
    for field in key_fields:
        # Support nested dicts via dot notation, e.g. "movement.gate"
        value = record
        for part in field.split("."):
            if isinstance(value, dict):
                value = value.get(part, "")
            else:
                value = ""
        key_parts.append(str(value))
    key_string = "_".join(key_parts)
    return hashlib.md5(key_string.encode("utf-8")).hexdigest()

def deduplicate_records(new_data: list[dict], upsert_runtime_vars: dict) -> list[dict]:
    if not new_data:
        print("⚠️ No records to deduplicate.")
        return new_data
    dedup_key = (
        upsert_runtime_vars.get("hash_id_name", "hash_id")
        if upsert_runtime_vars.get("hash_keys")
        else list(upsert_runtime_vars["fields_dict"].keys())[0]  
    )
    unique_data = {}
    for record in new_data:
        key = record.get(dedup_key)
        if key:
            unique_data[key] = record
        else:
            unique_data[id(record)] = record
    print(f"🧩 Deduplicated {len(new_data)} → {len(unique_data)} records")
    return list(unique_data.values())