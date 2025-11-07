CREATE TABLE IF NOT EXISTS cph_airport.flights
(
    transaction_id text COLLATE pg_catalog."default" NOT NULL,
    flight_number text COLLATE pg_catalog."default",
    scheduled_utc timestamp without time zone,
    airline text COLLATE pg_catalog."default",
    airline_iata text COLLATE pg_catalog."default",
    airline_icao text COLLATE pg_catalog."default",
    destination text COLLATE pg_catalog."default",
    destination_iata text COLLATE pg_catalog."default",
    destination_icao text COLLATE pg_catalog."default",
    scheduled_local timestamp without time zone,
    revised_utc timestamp without time zone,
    revised_local timestamp without time zone,
    runway_utc timestamp without time zone,
    runway_local timestamp without time zone,
    status text COLLATE pg_catalog."default",
    terminal text COLLATE pg_catalog."default",
    gate text COLLATE pg_catalog."default",
    aircraft_model text COLLATE pg_catalog."default",
    aircraft_reg text COLLATE pg_catalog."default",
    CONSTRAINT flights_pkey PRIMARY KEY (transaction_id)
)