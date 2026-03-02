select s.id_spools, s.initial_weight, 
s.initial_weight - coalesce(sum(u.weight_used), 0) as poid_restant
from public.spools as s
left join public.usage_logs as u on s.id_spools = u.id_spools 
where s.id_spools = 1
group by s.id_spools , s.initial_weight 

