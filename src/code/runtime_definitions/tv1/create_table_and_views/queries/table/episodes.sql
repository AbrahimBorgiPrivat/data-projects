CREATE TABLE IF NOT EXISTS tv_one.episodes
(
    episode_id bigint NOT NULL,
    program_id bigint,
    season_id bigint,
    title text COLLATE pg_catalog."default",
    details text COLLATE pg_catalog."default",
    url text COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    image text COLLATE pg_catalog."default",
    CONSTRAINT episodes_pkey PRIMARY KEY (episode_id)
)