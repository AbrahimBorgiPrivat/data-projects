CREATE TABLE IF NOT EXISTS gamma_db.posteringer
(
    id text COLLATE pg_catalog."default" NOT NULL,
    date date,
    text text COLLATE pg_catalog."default",
    amount double precision,
    bank_account_key text COLLATE pg_catalog."default",
    mp_key text COLLATE pg_catalog."default",
    user_id text COLLATE pg_catalog."default",
    account_number text COLLATE pg_catalog."default",
    posting_group_id text COLLATE pg_catalog."default",
    document text COLLATE pg_catalog."default",
    belongs_to_last_year boolean,
    CONSTRAINT posteringer_pkey PRIMARY KEY (id)
)