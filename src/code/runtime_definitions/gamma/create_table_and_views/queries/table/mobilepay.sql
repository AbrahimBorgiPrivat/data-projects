CREATE TABLE IF NOT EXISTS gamma_db.mobilepay
(
    id text COLLATE pg_catalog."default" NOT NULL,
    date date,
    timestamp_iso timestamp without time zone,
    amount double precision,
    message text COLLATE pg_catalog."default",
    transaction_type text COLLATE pg_catalog."default",
    transfer_ref text COLLATE pg_catalog."default",
    transfer_date date,
    merchant_name text COLLATE pg_catalog."default",
    receiver_acct text COLLATE pg_catalog."default",
    payment_tx_id text COLLATE pg_catalog."default",
    payner_name text COLLATE pg_catalog."default",
    payer_phone text COLLATE pg_catalog."default",
    CONSTRAINT mobilepay_pkey PRIMARY KEY (id)
)