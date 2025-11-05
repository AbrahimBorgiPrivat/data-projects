CREATE TABLE IF NOT EXISTS tv_one.programs
(
    program_id bigint NOT NULL,
    title text COLLATE pg_catalog."default",
    category text COLLATE pg_catalog."default",
    seasons bigint,
    url text COLLATE pg_catalog."default",
    image text COLLATE pg_catalog."default",
    CONSTRAINT programs_pkey PRIMARY KEY (program_id)
)