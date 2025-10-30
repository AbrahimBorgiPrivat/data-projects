from libraries.classes.database_client import DatabaseClient
from libraries.packages.client_to_client import read_sql_file
from libraries.packages.upsert_data import upsert_insert
from libraries.utils import path_config
from datetime import datetime
import os
import pandas as pd

def save_list_of_dicts_to_csv(data, output_dir="/app/backup", filename_prefix="backup"):
    if not data:
        print("No data to save.")
        return None
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.csv"
    full_path = os.path.join(output_dir, filename)
    df = pd.DataFrame(data)
    df.to_csv(full_path, index=False, sep=";")
    print(f"CSV file saved: {full_path}")
    return full_path

def from_client_to_csv(client: DatabaseClient, 
                                 upsert_runtime_vars: dict):
    sql_query = read_sql_file(path_config.RUNTIME_PATH / upsert_runtime_vars["sql_query"])
    new_data = client.get_data(sql_query)
    save_list_of_dicts_to_csv(new_data,
                              output_dir=upsert_runtime_vars["output_dir"],
                              filename_prefix=upsert_runtime_vars['filename_prefix'])
    