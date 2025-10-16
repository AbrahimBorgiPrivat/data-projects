from packages.upsert_data import from_client_to_client_upsert, build_client
from utils import env, runtime, path_config

def main(upsert_runtime_vars: dict):
    old_client = build_client(db_name=env.GAMMA_DB,
                          username=env.GAMMA_USERNAME,
                          password=env.GAMMA_PASSWORD,
                          server = env.GAMMA_HOST,
                          port=env.GAMMA_PORT,
                          db_type=env.GAMMA_DB_TYPE)
    new_client = build_client(db_name=env.POSTGRES_DB,
                          username=env.POSTGRES_USERNAME,
                          password=env.POSTGRES_PASSWORD,
                          server = env._POSTGRES_HOST,
                          port=env.POSTGRES_PORT,
                          db_type=env.DB_TYPE)
    from_client_to_client_upsert(old_client=old_client,
                                 new_client=new_client,
                                 upsert_runtime_vars=upsert_runtime_vars)

if __name__ == "__main__":
    path = path_config.RUNTINE_PATH / "gamma" / "users_runtime_def.json"
    upsert_runtime_vars = runtime.load_runtime_vars(JSON_PATH=path)
    main(upsert_runtime_vars)
