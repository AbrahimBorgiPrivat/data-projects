CREATE TABLE IF NOT EXISTS gamma_db.users
(
    id text COLLATE pg_catalog."default" NOT NULL,
    email text COLLATE pg_catalog."default",
    name text COLLATE pg_catalog."default",
    status bigint,
    aargang text COLLATE pg_catalog."default",
    occopation text COLLATE pg_catalog."default",
    last_payment timestamp without time zone,
    created timestamp without time zone,
    CONSTRAINT users_pkey PRIMARY KEY (id)
)