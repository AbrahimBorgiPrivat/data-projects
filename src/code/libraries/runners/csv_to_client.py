from libraries.packages.upsert_data import build_client
from libraries.packages.csv_to_client import csv_to_client_upsert
from libraries.utils import runtime,path_config
from libraries.utils.env import POSTGRES_DB

def main(upsert_runtime_vars: dict):
    client = build_client(db_name=upsert_runtime_vars['client']['db_name'],
                          username=upsert_runtime_vars['client']['username'],
                          password=upsert_runtime_vars['client']['password'],
                          server = upsert_runtime_vars['client']['server'],
                          port=upsert_runtime_vars['client']['port'],
                          db_type=upsert_runtime_vars['client']['db_type'])
    csv_to_client_upsert(client=client,
                                  upsert_runtime_vars=upsert_runtime_vars)
    
if __name__ == "__main__":
    path = path_config.RUNTIME_PATH / "gamma" / "csv_to_client" / "runtime" / "mobile_pay_runtime_def.json"
    upsert_runtime_vars = runtime.load_runtime_vars(JSON_PATH=path)
    main(upsert_runtime_vars)
