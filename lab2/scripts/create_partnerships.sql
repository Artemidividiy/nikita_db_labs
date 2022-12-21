-- Table: public.partnerships

-- DROP TABLE IF EXISTS public.partnerships;

CREATE TABLE IF NOT EXISTS public.partnerships
(
    id bigint NOT NULL,
    owner bigint NOT NULL,
    cooperative bigint NOT NULL,
    date timestamp without time zone NOT NULL,
    registration_data integer NOT NULL,
    pie_size double precision NOT NULL,
    CONSTRAINT partnerships_pkey PRIMARY KEY (id),
    CONSTRAINT cooperative FOREIGN KEY (cooperative)
        REFERENCES public.cooperatives (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT owner FOREIGN KEY (owner)
        REFERENCES public.owners (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.partnerships
    OWNER to postgres;