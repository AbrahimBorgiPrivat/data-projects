import hashlib
from collections import OrderedDict
import json
import hashlib
from collections import OrderedDict


def map_rows(
        rows: list[dict],
        mapping: list[dict],
        *,
        defaults: dict | None = None,
        pk_from: list[str] | None = None,
        pk_name: str = "id",
        column_order: list[str] | None = None,
        strict_columns: bool = True,
    ) -> list[dict]:
    def _to_string(v): return None if v is None else str(v)
    def _to_int(v): 
        try: return int(v)
        except Exception: return None
    def _to_float(v): 
        try: return float(v)
        except Exception: return None
    def _to_bool(v):
        if isinstance(v, bool): return v
        if isinstance(v, str): return v.strip().lower() in ("true", "1", "yes", "y")
        return bool(v)
    def _to_decimal(v):
        try: return float(v)
        except Exception: return None
    def _to_json(v):
        if v is None:
            return None
        if isinstance(v, (dict, list)):
            return v
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # return as-is if it’s not valid JSON text
                return v
        return v

    _TYPE_REGISTRY = {
        "string": lambda v, **kw: _to_string(v),
        "text":   lambda v, **kw: _to_string(v),
        "int":    lambda v, **kw: _to_int(v),
        "float":  lambda v, **kw: _to_float(v),
        "double": lambda v, **kw: _to_float(v),
        "decimal":lambda v, **kw: _to_decimal(v),
        "bool":   lambda v, **kw: _to_bool(v),
        "json":   lambda v, **kw: _to_json(v),     
        "dk_decimal":   lambda v, **kw: _to_decimal(v),
        "date_iso":     lambda v, **kw: _to_string(v),  
        "datetime_iso": lambda v, **kw: _to_string(v)
    }

    out = []
    for r in rows:
        new_r = {}
        for rule in mapping:
            old = rule["former_key"]
            new = rule["new_key"]
            typ = rule.get("type", "string")
            fmt = rule.get("fmt")
            raw_val = r.get(old)
            conv = _TYPE_REGISTRY.get(typ)
            if conv is None:
                raise ValueError(f"Unknown type '{typ}' in mapping for key '{old}'")
            new_r[new] = conv(raw_val, fmt=fmt)
        if defaults:
            for k, v in defaults.items():
                new_r.setdefault(k, v)
        if pk_from:
            src = "|".join("" if new_r.get(k) is None else str(new_r.get(k)) for k in pk_from)
            new_r[pk_name] = hashlib.sha256(src.encode("utf-8")).hexdigest()
        if column_order:
            ordered = OrderedDict()
            for k in column_order:
                ordered[k] = new_r.get(k)
            if not strict_columns:
                for k, v in new_r.items():
                    if k not in ordered:
                        ordered[k] = v
            out.append(dict(ordered))
        else:
            out.append(new_r)
    return out
