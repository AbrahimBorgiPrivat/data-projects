import hashlib
from datetime import datetime
from collections import OrderedDict
from decimal import Decimal, InvalidOperation
from classes.database_client import DatabaseClient
from packages.upsert_data import upsert_insert
from utils.csv_convert import convert_csv_to_dict

def _to_string(v):
    return "" if v is None else str(v).strip()

def _to_int(v):
    s = _to_string(v)
    return None if s == "" else int(s)

def _to_float(v):
    s = _to_string(v)
    return None if s == "" else float(s)

def _to_decimal(v) -> Decimal | None:
    s = _to_string(v)
    return None if s == "" else Decimal(s)

def _dk_decimal(v) -> float | None:
    s = _to_string(v)
    if s == "":
        return None
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(Decimal(s))
    except (InvalidOperation, ValueError):
        return None

def _to_bool(v):
    s = _to_string(v).lower()
    if s in {"true", "1", "yes", "ja", "y"}:
        return True
    if s in {"false", "0", "no", "nej", "n"}:
        return False
    return None

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


def map_rows(
        rows: list[dict],
        mapping: list[dict],
        *,
        defaults: dict | None = None,
        pk_from: list[str] | None = None,
        pk_name: str = "id",
        column_order: list[str] | None = None,   # NEW
        strict_columns: bool = True,             # NEW: only return columns in column_order
    ) -> list[dict]:
    _TYPE_REGISTRY = {
        "string": lambda v, **kw: _to_string(v),
        "text":   lambda v, **kw: _to_string(v),
        "int":    lambda v, **kw: _to_int(v),
        "float":  lambda v, **kw: _to_float(v),
        "double": lambda v, **kw: _to_float(v),
        "decimal":lambda v, **kw: _to_decimal(v),
        "bool":   lambda v, **kw: _to_bool(v),
        "dk_decimal":   lambda v, **kw: _dk_decimal(v),
        "date_iso":     lambda v, **kw: _date_iso(v, fmt=kw.get("fmt")),
        "datetime_iso": lambda v, **kw: _datetime_iso(v, fmt=kw.get("fmt")),
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
                if k in new_r:
                    ordered[k] = new_r[k]
                else:
                    ordered[k] = None  
            if not strict_columns:
                for k, v in new_r.items():
                    if k not in ordered:
                        ordered[k] = v
            out.append(dict(ordered))
        else:
            out.append(new_r)
    return out


def csv_to_client_upsert(client: DatabaseClient, upsert_runtime_vars: dict):
    new_data = convert_csv_to_dict(
        upsert_runtime_vars["path"],
        delimiter=upsert_runtime_vars.get("delimiter", "\t"),
        subset=upsert_runtime_vars.get("subset"),
    )
    column_order = upsert_runtime_vars.get("column_order")
    if column_order is None and upsert_runtime_vars.get("use_fields_dict_order"):
        column_order = list(upsert_runtime_vars["fields_dict"].keys())
    new_data = map_rows(
        new_data,
        upsert_runtime_vars["mapping"],
        defaults=upsert_runtime_vars.get("defaults"),
        pk_from=upsert_runtime_vars.get("pk_from"),
        pk_name=upsert_runtime_vars.get("pk_name", "id"),
        column_order=column_order,
        strict_columns=upsert_runtime_vars.get("strict_columns", True),
    )
    upsert_insert(
        client=client,
        upsert_runtime_vars=upsert_runtime_vars,
       new_data=new_data
    )

