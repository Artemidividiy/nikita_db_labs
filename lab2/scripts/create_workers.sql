-- Table: public.workers

-- DROP TABLE IF EXISTS public.workers;

CREATE TABLE IF NOT EXISTS public.workers
(
    id bigint NOT NULL,
    first_name character varying COLLATE pg_catalog."default" NOT NULL,
    middle_name character varying COLLATE pg_catalog."default" NOT NULL,
    last_name character varying COLLATE pg_catalog."default" NOT NULL,
    is_owner boolean NOT NULL,
    partnership bigint,
    "position" character varying COLLATE pg_catalog."default" NOT NULL,
    salary character varying COLLATE pg_catalog."default" NOT NULL,
    passport bigint NOT NULL,
    CONSTRAINT workers_pkey PRIMARY KEY (id),
    CONSTRAINT partnership FOREIGN KEY (partnership)
        REFERENCES public.partnerships (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT passport FOREIGN KEY (passport)
        REFERENCES public.passports (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.workers
    OWNER to postgres;