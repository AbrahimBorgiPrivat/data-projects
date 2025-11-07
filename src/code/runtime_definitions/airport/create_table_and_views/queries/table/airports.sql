CREATE TABLE IF NOT EXISTS cph_airport.airports
(
    icao text COLLATE pg_catalog."default" NOT NULL,
    name text COLLATE pg_catalog."default",
    city text COLLATE pg_catalog."default",
    country text COLLATE pg_catalog."default",
    country_code text COLLATE pg_catalog."default",
    latitude numeric,
    longitude numeric,
    world_area_code bigint,
    city_name_geo_name_id bigint,
    country_name_geo_name_id bigint,
    CONSTRAINT airports_pkey PRIMARY KEY (icao)
)