-- Index: last_name_index

-- DROP INDEX IF EXISTS public.last_name_index;

CREATE INDEX IF NOT EXISTS last_name_index
    ON public.workers USING btree
    (last_name COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
