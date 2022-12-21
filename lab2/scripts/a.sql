select w.first_name as "имя", w.last_name as "фамилия", p.series as "серия", p."number" as "number"
from public.workers w
left join passports p on p.id = w.passport
