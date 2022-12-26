-- function: public:worker_to_owner()

-- validating every worker entity on passport correspondence

-- drop function public.check_passports() if exists;

create or replace function public.check_passports()
returns table (id bigint, first_name varchar, middle_name varchar, last_name varchar, is_owner boolean, partnership bigint, "position" varchar, salary varchar, passport bigint)
language 'plpgsql'
as $body$

declare 
    current_worker_id integer;
    workers_count integer;
	passport_record record;
	worker_record record;
begin
    select count(*) into workers_count from public.workers;
	create temp table if not exists target as select * from public.workers;
    for current_worker_id in (select w.id from public.workers w)
    loop
        raise notice 'checking worker: %', (select w.last_name from workers w where w.id = current_worker_id);
       	select * from workers w where w.id = current_worker_id into worker_record;
		select * from passports p where p.id = worker_record.passport into passport_record;
		if(passport_record.first_name != worker_record.first_name or passport_record.middle_name != worker_record.middle_name or passport_record.last_name != worker_record.last_name)
		then
			raise notice 'passport validation failed for %', (select w.last_name from workers w where w.id = current_worker_id);
			insert into target select * from workers w where w.id = current_worker_id;
		end if;
    end loop;
    return query (select * from target);
end;
$body$;

-- alter function public.check_passports() owner to postgres;