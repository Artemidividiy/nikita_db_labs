-- Table: public.owners

-- DROP TABLE IF EXISTS public.owners;

CREATE TABLE IF NOT EXISTS public.owners
(
    id bigint NOT NULL,
    full_name character varying COLLATE pg_catalog."default" NOT NULL,
    address character varying COLLATE pg_catalog."default" NOT NULL,
    region character varying COLLATE pg_catalog."default" NOT NULL,
    passport_data bigint,
    CONSTRAINT owners_pkey PRIMARY KEY (id),
    CONSTRAINT passport FOREIGN KEY (passport_data)
        REFERENCES public.passports (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.owners
    OWNER to postgres;