CREATE TABLE IF NOT EXISTS gamma_db.bank_account
(
    id text COLLATE pg_catalog."default" NOT NULL,
    date date,
    text text COLLATE pg_catalog."default",
    amount double precision,
    balance double precision,
    status text COLLATE pg_catalog."default",
    reconciled text COLLATE pg_catalog."default",
    CONSTRAINT bank_account_pkey PRIMARY KEY (id)
)