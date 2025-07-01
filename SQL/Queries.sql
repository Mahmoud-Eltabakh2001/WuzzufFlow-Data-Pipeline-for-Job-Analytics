select * from jobs;
select * from skills;

SELECT job_title,work_type,workplace,company_name,company_page,experience_level,yrs_of_exp,address,city,country 
FROM jobs WHERE job_title ILIKE '%data%'
ORDER BY RANDOM()
limit 10;

select experience_level , count(*) as "Jobs" 
from jobs 
group by experience_level
order by count(*) desc;

select work_type , count(*) as "Jobs" 
from jobs 
where work_type != \'Hybrid\' and work_type != \'On-site\' 
group by work_type 
order by count(*) desc;


select workplace , count(*) as "Jobs" 
from jobs 
where workplace != \'Part Time\' and  workplace != \'Internship\'  
group by workplace 
order by count(*) desc;

select country,count(*) as "Jobs" 
from Jobs group by country 
order by count(*) Desc 
limit 10;

select city,count(*) as "Jobs" 
from Jobs group by city 
order by count(*) Desc 
limit 10;

SELECT s.skills  
FROM skills s INNER JOIN jobs j 
ON s.job_id = j.id 
WHERE j.job_title ILIKE '%data%';