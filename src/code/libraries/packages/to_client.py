from pathlib import Path
from libraries.classes.database_client import DatabaseClient
from libraries.packages.upsert_data import upsert_insert
from libraries.utils import path_config
from libraries.packages.csv_to_client import map_rows
from libraries.utils.csv_convert import convert_csv_to_dict
from sqlalchemy import text

def read_sql_file(file_path: str) -> str:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"SQL file not found: {path}")
    return path.read_text(encoding="utf-8")

def from_client_to_client_upsert(old_client: DatabaseClient, 
                                 new_client: DatabaseClient, 
                                 upsert_runtime_vars: dict):
    sql_query = read_sql_file(path_config.RUNTIME_PATH / upsert_runtime_vars["sql_query"])
    new_data = old_client.get_data(sql_query)
    upsert_insert(client = new_client,
                  upsert_runtime_vars = upsert_runtime_vars,
                  new_data=new_data)
    
def run_sequence_of_queries(client: DatabaseClient,  
                            upsert_runtime_vars: dict):
    sql_queries = upsert_runtime_vars["sql_queries"]
    for sql_query in sql_queries:
        sql_query = read_sql_file(path_config.RUNTIME_PATH / sql_query)
        engine = client.get_engine()
        with engine.begin() as connection:
                    connection.execute(text(sql_query))

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