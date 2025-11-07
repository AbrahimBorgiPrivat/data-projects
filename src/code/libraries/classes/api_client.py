import requests
import hashlib
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from libraries.utils.env import API_MARKET_KEY

class GeneralAPIClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.headers = headers or {}

        if api_key:
            self.headers.setdefault("x-api-market-key", api_key)
        self.headers.setdefault("accept", "application/json")

    @staticmethod
    def safe_int(val):
        try:
            return int(val)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def generate_md5_id(key: str) -> str:
        return hashlib.md5(key.encode("utf-8")).hexdigest()

    def request(self, method: str, endpoint: str = "", params: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}".rstrip("/")
        resp = requests.request(method, url, headers=self.headers, params=params, timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.json()

    def fetch_paginated(
        self,
        endpoint_params: Dict[str, Any],
        record_path: List[str],
        mapping: Optional[Dict[str, str]] = None,
        record_transform: Optional[Callable[[Dict], Dict]] = None,
        fields_dict: Optional[Dict[str, Dict[str, Any]]] = None,
        limit_param: str = "rows",
        offset_param: str = "start",
        limit: int = 100,
        total_key: str = "nhits",
        max_pages: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        all_records = []
        params = dict(endpoint_params)
        params[limit_param] = 1
        resp = self.request("GET", params=params)
        total_count = resp.get(total_key, 0)
        offset = 0
        page = 0
        while offset < total_count:
            if max_pages and page >= max_pages:
                break
            params = dict(endpoint_params)
            params[limit_param] = limit
            params[offset_param] = offset
            data = self.request("GET", params=params)
            records = data
            for key in record_path:
                records = records.get(key, [])
            for rec in records:
                if record_transform:
                    rec = record_transform(rec)
                if mapping:
                    mapped = {}
                    for src_key, target_key in mapping.items():
                        val = rec.get(src_key, None)
                        if fields_dict and target_key in fields_dict and val is not None:
                            expected_type = fields_dict[target_key]["type"].upper()
                            if expected_type == "TEXT":
                                if not isinstance(val, str):
                                    val = str(val) if val is not None else None
                            elif expected_type in ("NUMERIC", "DOUBLE PRECISION"):
                                try:
                                    val = float(val)
                                except (ValueError, TypeError):
                                    val = None
                            elif expected_type in ("BIGINT", "INT", "INTEGER"):
                                try:
                                    val = int(float(val))
                                except (ValueError, TypeError):
                                    val = None
                            elif expected_type == "TIMESTAMP":
                                if not isinstance(val, str):
                                    val = None
                        mapped[target_key] = val
                    rec = {target_key: mapped.get(target_key, None) for target_key in mapping.values()}
                all_records.append(rec)
            offset += limit
            page += 1
            print(f"Fetched {len(all_records)} / {total_count}")
        return all_records

    def normalize_records(self, records: List[Dict], mapping: Dict[str, str], extra_fields: Optional[Dict[str, Callable]] = None):
        normalized = []
        for rec in records:
            new_rec = {mapping.get(k, k): v for k, v in rec.items()}
            if extra_fields:
                for new_field, func in extra_fields.items():
                    new_rec[new_field] = func(rec)
            normalized.append(new_rec)
        return normalized

    def fetch_time_intervals(
        self,
        endpoint_template: str,
        start_time: datetime,
        days: int = 1,
        interval_hours: int = 12,
        date_fmt: str = "%Y-%m-%dT%H:%M",
        param_builder: Optional[Callable[[datetime, datetime], Dict]] = None,
        response_handler: Optional[Callable[[Dict], List[Dict]]] = None,
        params: Optional[Dict] = None,  
        **kwargs
    ) -> List[Dict]:
        all_data = []
        for d in range(days):
            for hour in range(0, 24, interval_hours):
                dt_from = start_time.replace(hour=hour, minute=0)
                dt_to = dt_from.replace(hour=hour + interval_hours - 1, minute=59)
                date_from = dt_from.strftime(date_fmt)
                date_to = dt_to.strftime(date_fmt)
                endpoint = endpoint_template.format(date_from=date_from, date_to=date_to)
                request_params = param_builder(dt_from, dt_to) if param_builder else params or {}
                try:
                    resp = self.request("GET", endpoint, params=request_params, **kwargs)
                    if response_handler:
                        all_data.extend(response_handler(resp))
                    else:
                        all_data.append(resp)
                except Exception as e:
                    Exception(f"Error fetching interval: {e}")
        return all_data


"""
api = GeneralAPIClient(
    base_url="https://public.opendatasoft.com/api/records/1.0/search/",
    headers={
        "accept": "application/json"
    }
)
airports = api.fetch_paginated(
    endpoint_params={"dataset": "airports-code@public"},
    record_path=["records"],
    record_transform=lambda rec: rec.get("fields", {}),  # extract inner "fields"
    mapping={"column_1": "icao",
            "airport_name": "name",
            "city_name": "city",
            "country_name": "country",
            "country_code": "country_code",
            "latitude": "latitude",
            "longitude": "longitude",
            "world_area_code": "world_area_code",
            "city_name_geo_name_id": "city_geo_id",
            "country_name_geo_name_id": "country_geo_id"
        },
    limit=200  
)
print(f"Fetched {len(airports)} airports")
print(airports[0:3])
"""