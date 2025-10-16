import logging
import json
import threading
import time
from typing import List, Dict
import sys
import io
import csv
from sqlalchemy import create_engine, text, MetaData, Column, Table
from sqlalchemy.engine import Engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy.exc import SQLAlchemyError, NoSuchTableError
from urllib.parse import quote_plus

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DatabaseClient:
    _engines: Dict[str, Engine] = {}
    _lock = threading.Lock()

    def __init__(
        self,
        db_name: str,
        username: str,
        password: str,
        server: str,
        port: int,
        db_type: str = "postgresql",
        pool_size: int = 10,
        max_overflow: int = 5,
    ):
        self.db_config = {
            "db_name": db_name,
            "username": quote_plus(username),
            "password": quote_plus(password),
            "server": server,
            "port": port,
            "db_type": db_type,
        }
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        driver = {
            "postgresql": "postgresql+psycopg2",
            "mysql": "mysql+pymysql"
        }.get(db_type, db_type)

        self.engine_key = f"{driver}://{quote_plus(username)}@{server}:{port}/{db_name}"

    def get_engine(self) -> Engine:
        """
        Returns a shared engine from the internal cache.
        Ensures only one engine per unique connection string.
        """
        with self._lock:
            if self.engine_key not in self._engines:
                logger.info(
                    f"[DatabaseClient] Creating new engine for {self.engine_key}"
                )
                driver = {
                    "postgresql": "postgresql+psycopg2",
                    "mysql": "mysql+pymysql"
                }.get(self.db_config["db_type"], self.db_config["db_type"])

                url = (
                    f"{driver}://{self.db_config['username']}:{self.db_config['password']}"
                    f"@{self.db_config['server']}:{self.db_config['port']}/{self.db_config['db_name']}"
                )
                self._engines[self.engine_key] = create_engine(
                    url,
                    pool_size=self.pool_size,
                    max_overflow=self.max_overflow,
                    future=True,
                )
            return self._engines[self.engine_key]

    def get_data(
        self, sql_query: str, retries: int = 3, delay: int = 2, timeout: int = 60
    ) -> List[Dict]:
        """
        Executes a SQL query with retries and timeout protection.
        """
        engine = self.get_engine()
        attempt = 0

        while attempt <= retries:
            result_data = []
            query_exception = None

            def execute_query():
                nonlocal result_data, query_exception
                try:
                    with engine.connect() as conn:
                        result = conn.execute(text(sql_query))
                        columns = result.keys()
                        result_data = [dict(zip(columns, row)) for row in result]
                except Exception as e:
                    query_exception = e

            thread = threading.Thread(target=execute_query, daemon=True)
            thread.start()
            thread.join(timeout=timeout)

            if thread.is_alive():
                logger.warning(
                    f"[DatabaseClient] Query timed out (attempt {attempt + 1}/{retries})"
                )
                attempt += 1
                time.sleep(delay)
                continue

            if query_exception:
                logger.error(f"[DatabaseClient] Query failed: {query_exception}")
                if attempt < retries:
                    attempt += 1
                    time.sleep(delay)
                    continue
                else:
                    raise query_exception

            return result_data

        raise RuntimeError("All retry attempts failed")

    def update_insert_dw(
        self,
        schema: str,
        table: str,
        new_data: List[Dict],
        pk: List[str],
        update_fields: List[str],
        not_included_in_update_fields: List[str] = [],
    ) -> int:
        """
        Perform a batch UPSERT (insert/update on conflict) operation.
        """
        if not new_data:
            logger.info("[DatabaseClient] No data to upsert.")
            return 0

        engine = self.get_engine()
        meta = MetaData(schema=schema)
        meta.reflect(bind=engine)

        upserts = len(new_data)
        columns = new_data[0].keys()

        insert_values = ", ".join(
            [
                f"({', '.join([f':{col}_{i}' for col in columns])})"
                for i in range(1, upserts + 1)
            ]
        )

        pk_clause = ", ".join(pk)
        insert_clause = ", ".join(pk + update_fields)
        only_update_fields = [
            field
            for field in update_fields
            if field not in not_included_in_update_fields
        ]

        if not update_fields:
            stmt = f"""
                INSERT INTO {schema}.{table} ({insert_clause})
                VALUES {insert_values}
                ON CONFLICT ({pk_clause}) DO NOTHING
            """
        else:
            update_clause = ", ".join(
                [f"{field} = EXCLUDED.{field}" for field in only_update_fields]
            )
            stmt = f"""
                INSERT INTO {schema}.{table} ({insert_clause})
                VALUES {insert_values}
                ON CONFLICT ({pk_clause}) DO UPDATE SET {update_clause}
            """

        # Prepare parameter bindings
        params = {}
        for i, row in enumerate(new_data, start=1):
            for column, value in row.items():
                key = f"{column}_{i}"
                if isinstance(value, (dict, list)):
                    params[key] = json.dumps(value)
                elif value is None:
                    params[key] = None
                else:
                    params[key] = value

        logger.info(f"[DatabaseClient] Upserting {upserts} rows into {schema}.{table}")
        try:
            with engine.begin() as connection:
                connection.execute(text(stmt), params)
            return upserts
        except SQLAlchemyError as e:
            logger.exception(f"[DatabaseClient] UPSERT failed: {e}")
            raise
    
    def check_schema_exists(self, 
                            schema_name: str,
                            create_schema_if_not_exist: bool):
        engine = self.get_engine()
        result = self.get_data(sql_query=f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema_name}'")
        exists = len(result) != 0
        print(exists)
        if not exists:
            if create_schema_if_not_exist:
                logger.info(f"Creating schema '{schema_name}'...")
                with engine.begin() as connection:
                    connection.execute(CreateSchema(schema_name))
                logger.info(f"Schema '{schema_name}' created.")
            else: 
                raise RuntimeError(
                    f"Table '{schema_name}' does not exist."
                )
        else: 
            logger.info(f"Schema '{schema_name}' exists: {exists}")
    
    def check_table_exist(self, 
                            schema_name: str,
                            table_name: str,
                            fields_dict: dict[str],
                            create_tale_if_not_exist: bool):
        engine = self.get_engine()
        try:
            logger.info(f"Checking for existing table '{schema_name}.{table_name}'...")
            metadata = MetaData(schema=schema_name)
            existing_table =  Table(table_name, metadata, autoload_with=engine)
            existing_columns = {
                                    col.name.lower(): type(col.type) for col in existing_table.columns
                                }
            existing_primary_keys = {
                                    col.name.lower() for col in existing_table.primary_key.columns
                                }
            input_columns = {}
            input_primary_keys = set()

            for col_name, col_info in fields_dict.items():
                col_type = col_info["type"] if isinstance(col_info, dict) else col_info
                input_columns[col_name.lower()] = type(col_type)
                if isinstance(col_info, dict) and col_info.get("primary_key", False):
                    input_primary_keys.add(col_name.lower())
            for col, expected_type in input_columns.items():
                if col not in existing_columns:
                    raise RuntimeError(f"Missing column '{col}' in table.")
                
                actual_type = existing_columns[col].__name__.lower()
                expected_type_str = expected_type.__name__.lower()
                if actual_type != expected_type_str:
                    raise RuntimeError(
                        f"Type mismatch for column '{col}': expected '{expected_type_str}', got '{actual_type}'."
                    )
                
            if existing_primary_keys != input_primary_keys:
                raise RuntimeError(
                    f"Primary key mismatch: expected {input_primary_keys}, got {existing_primary_keys}"
                )
            logger.info("Table structure is valid.")
                
        except NoSuchTableError:  # FOR NOW THIS WILL BE KEPT IN AS A FALL BACK
            if not create_tale_if_not_exist:
                raise RuntimeError(
                    f"Table '{schema_name}.{table_name}' does not exist."
                )
            logger.info(f"Creating table '{schema_name}.{table_name}'...")
            metadata = MetaData(schema=schema_name)
            columns = []
            for name, col_info in fields_dict.items():
                col_type = col_info["type"] if isinstance(col_info, dict) else col_info
                is_pk = isinstance(col_info, dict) and col_info.get("primary_key", False)
                kwargs = {"primary_key": is_pk}
                if isinstance(col_info, dict) and "autoincrement" in col_info:
                    kwargs["autoincrement"] = col_info["autoincrement"]
                columns.append(Column(name, col_type, **kwargs))

            table = Table(table_name, metadata, *columns)
            table.create(bind=engine)
            logger.info(
                f"Created table '{schema_name}.{table_name}' with columns: {list(fields_dict.keys())}"
            )
        
    def ensure_table_structure(
        self,
        schema_name: str,
        table_name: str,
        fields_dict: dict[str],
        create_tale_if_not_exist: bool
    ):
        logger.info(
            f"Ensuring table structure for '{schema_name}.{table_name}'"
        )

        try:
            self.check_schema_exists(schema_name=schema_name,
                                     create_schema_if_not_exist=create_tale_if_not_exist)

            self.check_table_exist(schema_name=schema_name,
                                   table_name=table_name,
                                   fields_dict=fields_dict,
                                   create_tale_if_not_exist=create_tale_if_not_exist)
            return True
        except Exception as e:
            logger.error(f"Failed to ensure table structure: {e}")
            raise

    def copy_to_staging_table(
        self, schema: str, staging_table: str, data: list[dict], columns: list[str]
    ):
        """
        Fast bulk insert into a staging table using PostgreSQL COPY.
        """
        if not data:
            logger.info("No data to copy.")
            return

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)
        output.seek(0)

        table_ref = f'"{schema}"."{staging_table}"'

        engine = self.get_engine()
        conn = engine.raw_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.copy_expert(
                    f"COPY {table_ref} ({', '.join(columns)}) FROM STDIN WITH CSV HEADER",
                    output,
                )
                conn.commit()
                logger.info(f"Copied {len(data)} rows into {table_ref}")
            except Exception as e:
                conn.rollback()
                logger.exception(f"COPY to staging failed: {e}")
                raise
            finally:
                cursor.close()
        finally:
            conn.close()

    def merge_staging_to_target(
        self,
        schema: str,
        staging_table: str,
        target_table: str,
        columns: list[str],
        pk_columns: list[str],
        update_columns: list[str],
    ):
        """
        Performs UPSERT (merge) from staging table to target table.
        """
        target_ref = f'"{schema}"."{target_table}"'
        staging_ref = f'"{schema}"."{staging_table}"'

        insert_cols = ", ".join(columns)
        conflict_cols = ", ".join(pk_columns)
        update_clause = ", ".join([f"{col} = EXCLUDED.{col}" for col in update_columns])

        sql = f"""
        INSERT INTO {target_ref} ({insert_cols})
        SELECT {insert_cols} FROM {staging_ref}
        ON CONFLICT ({conflict_cols}) DO UPDATE SET {update_clause};
        """

        engine = self.get_engine()
        try:
            with engine.begin() as conn:
                conn.execute(text(sql))
                logger.info(f"Merged data from {staging_ref} into {target_ref}")
        except Exception as e:
            logger.info(f'Error: {e}')

    def truncate_table(self, schema: str, table: str):
        engine = self.get_engine()
        try:
            with engine.begin() as conn:
                sql = text(f'TRUNCATE TABLE "{schema}"."{table}" RESTART IDENTITY CASCADE')
                conn.execute(sql)
                logger.info(f"Truncated table {schema}.{table}")
        except Exception as e:
            logger.exception(f"[DatabaseClient] Failed truncating table {schema}.{table}: {e}")
            raise

