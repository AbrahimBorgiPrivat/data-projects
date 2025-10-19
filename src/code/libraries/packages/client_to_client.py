from classes.database_client import DatabaseClient
from .upsert_data import upsert_insert
from pathlib import Path
from utils import path_config

def read_sql_file(file_path: str) -> str:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"SQL file not found: {path}")
    return path.read_text(encoding="utf-8")

def from_client_to_client_upsert(old_client: DatabaseClient, 
                                 new_client: DatabaseClient, 
                                 upsert_runtime_vars: dict):
    sql_query = read_sql_file(path_config.RUNTINE_PATH / upsert_runtime_vars["sql_query"])
    new_data = old_client.get_data(sql_query)
    upsert_insert(client = new_client,
                  upsert_runtime_vars = upsert_runtime_vars,
                  new_data=new_data)