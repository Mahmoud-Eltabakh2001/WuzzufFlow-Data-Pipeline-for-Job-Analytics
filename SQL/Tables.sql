DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS jobs;

CREATE TABLE jobs (
    id INT PRIMARY KEY,         
    job_title VARCHAR(100),
    work_type VARCHAR(50),
    workplace VARCHAR(50),
    company_name VARCHAR(100),
    company_page VARCHAR(250),
    experience_level VARCHAR(100),
    yrs_of_exp VARCHAR(100),
    address VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE skills (
    id INT PRIMARY KEY,   
    job_id INT REFERENCES jobs(id),
    skills VARCHAR
);


