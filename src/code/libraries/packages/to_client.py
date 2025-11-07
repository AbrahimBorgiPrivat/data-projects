from pathlib import Path
from sqlalchemy import text
from datetime import datetime
from typing import Optional

import json

from libraries.classes.database_client import DatabaseClient
from libraries.classes.api_client import GeneralAPIClient
from libraries.packages.upsert_data import upsert_insert, build_client
from libraries.packages.csv_to_client import map_rows
from libraries.utils import path_config, api_handlers
from libraries.utils.csv_convert import convert_csv_to_dict

def read_sql_file(file_path: str) -> str:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"SQL file not found: {path}")
    return path.read_text(encoding="utf-8")

def from_client_to_client_upsert(upsert_runtime_vars: dict,
                                 old_client: Optional[DatabaseClient] = None,
                                 new_client: Optional[DatabaseClient] = None):
    if old_client is None:
        old_client = build_client(db_name=upsert_runtime_vars['old_client']['db_name'],
                                    username=upsert_runtime_vars['old_client']['username'],
                                    password=upsert_runtime_vars['old_client']['password'],
                                    server = upsert_runtime_vars['old_client']['server'],
                                    port=upsert_runtime_vars['old_client']['port'],
                                    db_type=upsert_runtime_vars['old_client']['db_type'])
    if new_client is None:
        new_client = build_client(db_name=upsert_runtime_vars['new_client']['db_name'],
                                    username=upsert_runtime_vars['new_client']['username'],
                                    password=upsert_runtime_vars['new_client']['password'],
                                    server = upsert_runtime_vars['new_client']['server'],
                                    port=upsert_runtime_vars['new_client']['port'],
                                    db_type=upsert_runtime_vars['new_client']['db_type'])
    
    sql_query = read_sql_file(path_config.RUNTIME_PATH / upsert_runtime_vars["sql_query"])
    new_data = old_client.get_data(sql_query)
    upsert_insert(client = new_client,
                  upsert_runtime_vars = upsert_runtime_vars,
                  new_data=new_data)
    
def run_sequence_of_queries(upsert_runtime_vars: dict,
                            client: Optional[DatabaseClient] = None):
    if client is None:
        client = build_client(db_name=upsert_runtime_vars['client']['db_name'],
                            username=upsert_runtime_vars['client']['username'],
                            password=upsert_runtime_vars['client']['password'],
                            server = upsert_runtime_vars['client']['server'],
                            port=upsert_runtime_vars['client']['port'],
                            db_type=upsert_runtime_vars['client']['db_type'])
    sql_queries = upsert_runtime_vars["sql_queries"]
    for sql_query in sql_queries:
        sql_query = read_sql_file(path_config.RUNTIME_PATH / sql_query)
        engine = client.get_engine()
        with engine.begin() as connection:
                    connection.execute(text(sql_query))

def json_to_client(upsert_runtime_vars: dict,
                   client: Optional[DatabaseClient] = None):
    if client is None:
        client = build_client(db_name=upsert_runtime_vars['client']['db_name'],
                            username=upsert_runtime_vars['client']['username'],
                            password=upsert_runtime_vars['client']['password'],
                            server = upsert_runtime_vars['client']['server'],
                            port=upsert_runtime_vars['client']['port'],
                            db_type=upsert_runtime_vars['client']['db_type'])
    json_path = path_config.RES_PATH / upsert_runtime_vars["path"]
    if not json_path.exists():
        raise FileNotFoundError(f"[ERROR] JSON file not found: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        new_data = json.load(f)
    if not isinstance(new_data, list):
        raise ValueError("[ERROR] Expected a JSON array (list of dicts).")
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
    return upsert_insert(client=client,
            upsert_runtime_vars=upsert_runtime_vars,
            new_data=new_data
        )

def csv_to_client_upsert(upsert_runtime_vars: dict,
                         client: Optional[DatabaseClient] = None):
    if client is None:
        client = build_client(db_name=upsert_runtime_vars['client']['db_name'],
                            username=upsert_runtime_vars['client']['username'],
                            password=upsert_runtime_vars['client']['password'],
                            server = upsert_runtime_vars['client']['server'],
                            port=upsert_runtime_vars['client']['port'],
                            db_type=upsert_runtime_vars['client']['db_type'])
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

def api_fetch_paginated_to_client_upser(upsert_runtime_vars: dict):
    client = build_client(db_name=upsert_runtime_vars['client']['db_name'],
                          username=upsert_runtime_vars['client']['username'],
                          password=upsert_runtime_vars['client']['password'],
                          server = upsert_runtime_vars['client']['server'],
                          port=upsert_runtime_vars['client']['port'],
                          db_type=upsert_runtime_vars['client']['db_type'])
    api = GeneralAPIClient(
        base_url=upsert_runtime_vars["base_url"],
        headers=upsert_runtime_vars["headers"]
    )
    new_data = api.fetch_paginated(
            endpoint_params=upsert_runtime_vars["endpoint_params"],
            record_path=upsert_runtime_vars["record_path"],
            record_transform = api_handlers.load_handler(upsert_runtime_vars["record_transform"]["path"],
                                                        upsert_runtime_vars["record_transform"]["func"]),  
            mapping=upsert_runtime_vars["mapping"],
            fields_dict=upsert_runtime_vars["fields_dict"],
            limit=upsert_runtime_vars["limit"]
    )
    upsert_insert(
        client=client,
        upsert_runtime_vars=upsert_runtime_vars,
        new_data=new_data
    )
    return new_data

def api_time_interval_to_client_upsert(upsert_runtime_vars: dict):
    client = build_client(db_name=upsert_runtime_vars['client']['db_name'],
                          username=upsert_runtime_vars['client']['username'],
                          password=upsert_runtime_vars['client']['password'],
                          server = upsert_runtime_vars['client']['server'],
                          port=upsert_runtime_vars['client']['port'],
                          db_type=upsert_runtime_vars['client']['db_type'])
    api = GeneralAPIClient(
        base_url=upsert_runtime_vars["base_url"],
        headers=upsert_runtime_vars["headers"]
    )
    new_data = api.fetch_time_intervals(
        endpoint_template = upsert_runtime_vars.get("endpoint_template"),
        start_time = datetime.fromisoformat(upsert_runtime_vars.get("start_time")) if upsert_runtime_vars.get("start_time") else datetime.now(),
        days = upsert_runtime_vars.get("days",1),
        interval_hours = upsert_runtime_vars.get("interval_hours",12),
        response_handler = api_handlers.load_handler(upsert_runtime_vars["response_handler"]["path"],
                                                    upsert_runtime_vars["response_handler"]["func"]),
        params = upsert_runtime_vars.get("params")
    )
    if upsert_runtime_vars.get("hash_keys"):
        hash_keys = upsert_runtime_vars["hash_keys"]
        hash_field_name = upsert_runtime_vars.get("hash_id_name", "hash_id")
        for record in new_data:
            record[hash_field_name] = api_handlers._generate_hash_id(record, hash_keys)
        for i, record in enumerate(new_data):
            new_data[i] = {hash_field_name: record.pop(hash_field_name), **record}
    if upsert_runtime_vars.get("remove_duplicate")==True:
        new_data = api_handlers.deduplicate_records(new_data,upsert_runtime_vars)
    upsert_insert(
        client=client,
        upsert_runtime_vars=upsert_runtime_vars,
        new_data=new_data
    )
    return new_data