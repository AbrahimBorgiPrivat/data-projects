from libraries.packages.upsert_data import build_client
from libraries.packages.client_to_csv import from_client_to_csv
from libraries.utils import runtime, path_config

def main(upsert_runtime_vars: dict):
    client = build_client(db_name=upsert_runtime_vars['client']['db_name'],
                          username=upsert_runtime_vars['client']['username'],
                          password=upsert_runtime_vars['client']['password'],
                          server = upsert_runtime_vars['client']['server'],
                          port=upsert_runtime_vars['client']['port'],
                          db_type=upsert_runtime_vars['client']['db_type'])
    from_client_to_csv(client=client,
                        upsert_runtime_vars=upsert_runtime_vars)

if __name__ == "__main__":
    path = path_config.RUNTIME_PATH / "gamma" / "client_to_csv" / "runtime" / "users.json"
    upsert_runtime_vars = runtime.load_runtime_vars(JSON_PATH=path)
    main(upsert_runtime_vars)
