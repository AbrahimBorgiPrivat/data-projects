CREATE TABLE IF NOT EXISTS cph_airport.passports
(
    passport_number text COLLATE pg_catalog."default" NOT NULL,
    name text COLLATE pg_catalog."default",
    country text COLLATE pg_catalog."default",
    CONSTRAINT passports_pkey PRIMARY KEY (passport_number)
)