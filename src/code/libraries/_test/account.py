from packages.upsert_data import build_client
from packages.bank_account import bank_account_to_client_upsert
from utils import env,runtime,path_config


def main(upsert_runtime_vars: dict):
    client = build_client(db_name=env.POSTGRES_DB,
                          username=env.POSTGRES_USERNAME,
                          password=env.POSTGRES_PASSWORD,
                          server = env._POSTGRES_HOST,
                          port=env.POSTGRES_PORT,
                          db_type=env.DB_TYPE)
    bank_account_to_client_upsert(client=client,
                                  upsert_runtime_vars=upsert_runtime_vars)
    
if __name__ == "__main__":
    path = path_config.RUNTINE_PATH / "gamma" / "upsert_mobile_pay_csv.json"
    upsert_runtime_vars = runtime.load_runtime_vars(JSON_PATH=path)
    main(upsert_runtime_vars)
