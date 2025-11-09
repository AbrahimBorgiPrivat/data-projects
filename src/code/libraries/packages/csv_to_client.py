import json
import hashlib
from collections import OrderedDict
from datetime import datetime
from decimal import Decimal, InvalidOperation

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
    def _dk_decimal(v) -> float | None:
        s = _to_string(v)
        if s == "":
            return None
        s = s.replace(".", "").replace(",", ".")
        try:
            return float(Decimal(s))
        except (InvalidOperation, ValueError):
            return None
    def _to_json(v):
        if v is None:
            return None
        if isinstance(v, (dict, list)):
            return v
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return v
        return v
    def _date_iso(v, fmt: str | None = None) -> str | None:
        s = _to_string(v)
        if s == "":
            return None
        fmts = [fmt] if fmt else ["%Y-%m-%d", "%d.%m.%Y", "%d-%m-%Y", "%d/%m/%Y"]
        for f in fmts:
            try:
                return datetime.strptime(s, f).date().isoformat()
            except ValueError:
                continue
        return None
    def _datetime_iso(v, fmt: str | None = None) -> str | None:
        s = _to_string(v)
        if s == "":
            return None
        if fmt:
            try:
                return datetime.strptime(s, fmt).isoformat(timespec="seconds")
            except ValueError:
                return None
        try:
            return datetime.fromisoformat(s).isoformat(timespec="seconds")
        except ValueError:
            pass
        # try a few DK combos
        for f in ("%d-%m-%Y %H:%M", "%d.%m.%Y %H:%M", "%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M"):
            try:
                return datetime.strptime(s, f).isoformat(timespec="seconds")
            except ValueError:
                continue
        return None

    _TYPE_REGISTRY = {
        "string": lambda v, **kw: _to_string(v),
        "text":   lambda v, **kw: _to_string(v),
        "int":    lambda v, **kw: _to_int(v),
        "float":  lambda v, **kw: _to_float(v),
        "double": lambda v, **kw: _to_float(v),
        "decimal":lambda v, **kw: _to_decimal(v),
        "bool":   lambda v, **kw: _to_bool(v),
        "json":   lambda v, **kw: _to_json(v),     
        "dk_decimal":   lambda v, **kw: _dk_decimal(v),
        "date_iso":     lambda v, **kw: _date_iso(v, fmt=kw.get("fmt")),
        "datetime_iso": lambda v, **kw: _datetime_iso(v, fmt=kw.get("fmt"))
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
