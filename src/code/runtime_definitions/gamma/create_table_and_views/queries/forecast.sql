CREATE TABLE IF NOT EXISTS gamma_db.forecast
(
    id text COLLATE pg_catalog."default" NOT NULL,
    account_id text COLLATE pg_catalog."default",
    postering_group_id text COLLATE pg_catalog."default",
    year_actual bigint,
    forecast double precision,
    forecast_type text COLLATE pg_catalog."default",
    CONSTRAINT forecast_pkey PRIMARY KEY (id)
)