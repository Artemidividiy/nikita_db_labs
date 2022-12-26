-- FUNCTION: public.all_cooperatives_capitals(bigint)

-- recieve all capitals from all cooperatives of owner

-- DROP FUNCTION IF EXISTS public.all_cooperatives_capitals(bigint);

CREATE OR REPLACE FUNCTION public.all_cooperatives_capitals(
	owner_id bigint)
    RETURNS varchar
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
declare 
    cooperative_id integer;
	capital numeric;
	target bigint;
begin
target := 0;
for cooperative_id in (select p.cooperative from public.partnerships p where p.owner = owner_id)
loop 
    raise notice 'cooperative %', cooperative_id;
	SELECT NULLIF(regexp_replace( c.capital , '\D','','g'), '')::numeric into capital from cooperatives c where c.id = cooperative_id;
	target := target + capital;
end loop;
return target::varchar || ' рублей';
end;
$BODY$;

ALTER FUNCTION public.all_cooperatives_capitals(bigint)
    OWNER TO postgres;
