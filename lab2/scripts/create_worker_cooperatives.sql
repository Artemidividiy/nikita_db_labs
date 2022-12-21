-- Table: public.workers_cooperatives

-- DROP TABLE IF EXISTS public.workers_cooperatives;

CREATE TABLE IF NOT EXISTS public.workers_cooperatives
(
    id bigint NOT NULL,
    worker bigint NOT NULL,
    cooperative bigint NOT NULL,
    CONSTRAINT workers_cooperatives_pkey PRIMARY KEY (id),
    CONSTRAINT cooperative FOREIGN KEY (cooperative)
        REFERENCES public.cooperatives (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT worker FOREIGN KEY (worker)
        REFERENCES public.workers (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.workers_cooperatives
    OWNER to postgres;