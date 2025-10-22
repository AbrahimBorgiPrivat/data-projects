CREATE TABLE IF NOT EXISTS gamma_db.postering_group
(
    id text COLLATE pg_catalog."default" NOT NULL,
    posting_group text COLLATE pg_catalog."default",
    posting_group_key bigint,
    posting_sub_group text COLLATE pg_catalog."default",
    posting_sub_group_key bigint,
    context text COLLATE pg_catalog."default",
    context_key bigint,
    CONSTRAINT postering_group_pkey PRIMARY KEY (id)
)