CREATE TABLE IF NOT EXISTS tv_one.seasons
(
    season_id bigint NOT NULL,
    program_id bigint,
    season bigint,
    url text COLLATE pg_catalog."default",
    CONSTRAINT seasons_pkey PRIMARY KEY (season_id)
)