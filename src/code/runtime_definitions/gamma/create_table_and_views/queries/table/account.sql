CREATE TABLE IF NOT EXISTS gamma_db.account
(
    id text COLLATE pg_catalog."default" NOT NULL,
    main_account text COLLATE pg_catalog."default",
    account_key bigint,
    sub_account text COLLATE pg_catalog."default",
    sub_account_key bigint,
    context text COLLATE pg_catalog."default",
    context_key bigint,
    CONSTRAINT account_pkey PRIMARY KEY (id)
)