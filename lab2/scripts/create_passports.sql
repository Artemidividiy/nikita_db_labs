-- Table: public.passports

-- DROP TABLE IF EXISTS public.passports;

CREATE TABLE IF NOT EXISTS public.passports
(
    first_name character varying COLLATE pg_catalog."default" NOT NULL,
    middle_name character varying COLLATE pg_catalog."default" NOT NULL,
    last_name character varying COLLATE pg_catalog."default" NOT NULL,
    place_code character varying COLLATE pg_catalog."default" NOT NULL,
    date_given timestamp without time zone NOT NULL,
    series integer NOT NULL,
    "number" integer NOT NULL,
    id bigint NOT NULL,
    CONSTRAINT passports_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.passports
    OWNER to postgres;