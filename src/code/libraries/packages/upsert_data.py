from classes.database_client import DatabaseClient
from utils.db_types import BIGINT, JSONB, INTEGER, TEXT, TIMESTAMP, BOOLEAN, ARRAY, Date, Float, DOUBLE_PRECISION

def build_client(
    db_name: str, username: str, password: str, server: str, port: int, db_type: str
    ) -> DatabaseClient:
        return DatabaseClient(
            db_name=db_name,
            username=username,
            password=password,
            server=server,
            port=port,
            db_type=db_type,
        )

def parse_fields_dict_from_json(fields_json):
    SQL_TYPE_MAP = {
        "BIGINT": BIGINT,
        "JSONB": JSONB,
        "INTEGER": INTEGER,
        "DOUBLE_PRECISION": DOUBLE_PRECISION,
        "TEXT": TEXT,
        "BOOLEAN": BOOLEAN,
        "TIMESTAMP": TIMESTAMP,
        "ARRAY": ARRAY,
        "DATE": Date,
        "FLOAT": Float
    }
    parsed = {}
    for col_name, props in fields_json.items():
        type_str = props.get("type")
        if type_str not in SQL_TYPE_MAP:
            raise ValueError(f"Unsupported type '{type_str}' in column '{col_name}'")
        sa_type = SQL_TYPE_MAP[type_str]()
        field_config = {"type": sa_type}
        for key, val in props.items():
            if key != "type":
                field_config[key] = val
        parsed[col_name] = field_config
    return parsed
    
def upsert_insert(client: DatabaseClient, 
                  upsert_runtime_vars: dict, 
                  new_data: list[dict]):
    
    fields_dict = parse_fields_dict_from_json(upsert_runtime_vars["fields_dict"])
    passed = client.ensure_table_structure(schema_name=upsert_runtime_vars["schema"],
                                           table_name=upsert_runtime_vars["table_name"],
                                           fields_dict=fields_dict,
                                           create_tale_if_not_exist=upsert_runtime_vars.get("create_table_if_not_exist", False)
                                           )
    if not passed:
        raise RuntimeError("Target table structure validation failed.")
    
    primary_keys = [k for k, v in upsert_runtime_vars["fields_dict"].items() if v.get("primary_key")]
    client.update_insert_dw(schema=upsert_runtime_vars["schema"],
                            table=upsert_runtime_vars["table_name"],
                            new_data=new_data,
                            pk=primary_keys,
                            update_fields=upsert_runtime_vars["update_fields"],
                            not_included_in_update_fields=upsert_runtime_vars["not_included_in_update_fields"])
                            
def from_client_to_client_upsert(old_client: DatabaseClient, 
                                 new_client: DatabaseClient, 
                                 upsert_runtime_vars: dict):
    new_data = old_client.get_data(upsert_runtime_vars["sql_query"])
    upsert_insert(client = new_client,
                  upsert_runtime_vars = upsert_runtime_vars,
                  new_data=new_data)
    
