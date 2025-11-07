CREATE TABLE IF NOT EXISTS cph_airport.tickets
(
    unique_id text COLLATE pg_catalog."default" NOT NULL,
    transaction_id text COLLATE pg_catalog."default",
    seat_number bigint,
    passport_number text COLLATE pg_catalog."default",
    check_in_type text COLLATE pg_catalog."default",
    checkin_time timestamp without time zone,
    passed_security_time timestamp without time zone,
    CONSTRAINT tickets_pkey PRIMARY KEY (unique_id)
)