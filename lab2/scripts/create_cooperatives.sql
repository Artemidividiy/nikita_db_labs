-- Table: public.cooperatives

-- DROP TABLE IF EXISTS public.cooperatives;

CREATE TABLE IF NOT EXISTS public.cooperatives
(
    name character varying COLLATE pg_catalog."default" NOT NULL,
    placement character varying COLLATE pg_catalog."default" NOT NULL,
    capital character varying COLLATE pg_catalog."default" NOT NULL,
    workers_count character varying COLLATE pg_catalog."default" NOT NULL,
    profile character varying COLLATE pg_catalog."default" NOT NULL,
    id bigint NOT NULL,
    CONSTRAINT cooperatives_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.cooperatives
    OWNER to postgres;