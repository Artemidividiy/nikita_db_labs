select * from workers w 
left join partnerships part on part.owner = w.id and w.position = 'менеджер'