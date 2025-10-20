from libraries.packages.upsert_data import build_client
from libraries.packages.client_to_client import from_client_to_client_upsert
from libraries.utils import runtime, path_config

def main(upsert_runtime_vars: dict):
    old_client = build_client(db_name=upsert_runtime_vars['old_client']['db_name'],
                          username=upsert_runtime_vars['old_client']['username'],
                          password=upsert_runtime_vars['old_client']['password'],
                          server = upsert_runtime_vars['old_client']['server'],
                          port=upsert_runtime_vars['old_client']['port'],
                          db_type=upsert_runtime_vars['old_client']['db_type'])
    new_client = build_client(db_name=upsert_runtime_vars['new_client']['db_name'],
                          username=upsert_runtime_vars['new_client']['username'],
                          password=upsert_runtime_vars['new_client']['password'],
                          server = upsert_runtime_vars['new_client']['server'],
                          port=upsert_runtime_vars['new_client']['port'],
                          db_type=upsert_runtime_vars['new_client']['db_type'])
    from_client_to_client_upsert(old_client=old_client,
                                 new_client=new_client,
                                 upsert_runtime_vars=upsert_runtime_vars)

if __name__ == "__main__":
    path = path_config.RUNTIME_PATH / "gamma" / "client_to_client" / "runtime" / "users_runtime_def.json"
    upsert_runtime_vars = runtime.load_runtime_vars(JSON_PATH=path)
    main(upsert_runtime_vars)
