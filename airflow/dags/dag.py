# dags/wuzzuf_dag.py

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "spark_jobs"))

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from docker.types import Mount
from datetime import datetime

from ge_validation import validate_data
from scrape_wuzzuf import scrape_wuzzuf


with DAG(
    dag_id="Wuzzaf.com",
    description="Scrape data from Wuzzuf.com and process with PySpark then load to Postgres",
    schedule_interval="@daily",
    start_date=datetime(2025, 6, 22),
    catchup=False,
    tags=["scraping"]
) as dag:
    
    # Scrap Wuzzuf.com
    scraping = PythonOperator(
        task_id="scraping",
        python_callable=scrape_wuzzuf,
    )

    #Load data to hdfs
    upload_to_hdfs = BashOperator(
        task_id="upload_to_hdfs",
        bash_command="""
        curl -i -L -X PUT "http://namenode:9870/webhdfs/v1/wuzzuf/Wuzzuf_data.csv?op=CREATE&overwrite=true&user.name=root" \
            -H "Content-Type: application/octet-stream" \
            -T /opt/airflow/dags/Wuzzuf_data.csv
        """
    )

    #Transform
    run_pyspark_job = DockerOperator(
        task_id="run_pyspark_transform",
        image="bitnami/spark:3.5",
        api_version="auto",
        auto_remove=True,
        command="/opt/bitnami/spark/bin/spark-submit /opt/airflow/spark_jobs/transform_wuzzuf.py",
        mounts=[
            Mount(
                source="/c/Docker_Project/airflow/spark_jobs",
                target="/opt/airflow/spark_jobs",
                type="bind"
            )
        ],
        mount_tmp_dir=False,
        network_mode="docker_project_hadoop"
    )

    #Validation data with Great Expectations
    validate_data_with_ge = DockerOperator(
        task_id='validate_data_with_gx',
        #image='spark',  
        image="custom-spark:latest",
        api_version='auto',
        auto_remove=True,
        command='python3 /opt/bitnami/spark_jobs/ge_validation.py',
        docker_url='unix://var/run/docker.sock',
        network_mode='docker_project_hadoop', 
        mounts=[
            Mount(
                source="/c/Docker_Project/airflow/spark_jobs",
                target="/opt/bitnami/spark_jobs",
                type="bind"
            ),
            Mount(
                source="/c/Docker_Project/airflow/validation_report",
                target="/opt/airflow/validation_report",
                type="bind"
            ),
        ],
        mount_tmp_dir=False
    ) 

    #Create Tables in Postgres db
    create_tables = PostgresOperator(
        task_id="create_tables",
        postgres_conn_id="postgres_conn",
        sql='''
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

        '''
    )

    #Load data to Postgres
    load_to_postgres = DockerOperator(
        task_id="load_data_to_postgres",
        image="custom-spark:latest", 
        api_version='auto',
        auto_remove=True,
        command="/opt/bitnami/spark/bin/spark-submit /opt/airflow/spark_jobs/load_to_postgres.py",

        docker_url="unix://var/run/docker.sock",
        network_mode="docker_project_hadoop",  
        mount_tmp_dir=False,
        mounts=[
            Mount(
                source="/c/Docker_Project/airflow/spark_jobs",
                target="/opt/airflow/spark_jobs",
                type="bind"
            ),
            Mount(
                source="/c/Docker_Project/airflow/validation_reports",
                target="/opt/airflow/validation_reports",
                type="bind"
            ),
        ],
    )

    #Task Dependencies
    scraping >> upload_to_hdfs >> run_pyspark_job >> validate_data_with_ge >> create_tables >> load_to_postgres
    
  