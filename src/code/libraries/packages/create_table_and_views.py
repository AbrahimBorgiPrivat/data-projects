from pathlib import Path
from libraries.classes.database_client import DatabaseClient
from libraries.utils import path_config
from sqlalchemy import text

def read_sql_file(file_path: str) -> str:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"SQL file not found: {path}")
    return path.read_text(encoding="utf-8")

def run_sequence_of_queries(client: DatabaseClient,  
                            upsert_runtime_vars: dict):
    sql_queries = upsert_runtime_vars["sql_queries"]
    for sql_query in sql_queries:
        sql_query = read_sql_file(path_config.RUNTIME_PATH / sql_query)
        engine = client.get_engine()
        with engine.begin() as connection:
                    connection.execute(text(sql_query))
        