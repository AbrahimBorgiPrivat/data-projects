CREATE TABLE IF NOT EXISTS cph_airport.aircraft_models
(
    aircraft_model text COLLATE pg_catalog."default" NOT NULL,
    manufacturer text COLLATE pg_catalog."default",
    country text COLLATE pg_catalog."default",
    seats bigint,
    range_km bigint,
    engine_type text COLLATE pg_catalog."default",
    icao_code text COLLATE pg_catalog."default",
    iata_code text COLLATE pg_catalog."default",
    CONSTRAINT aircraft_models_pkey PRIMARY KEY (aircraft_model)
)