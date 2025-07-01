# 📊 WuzzufFlow: A Dockerized Data Pipeline for Job Analytics
WuzzufFlow is an end-to-end data engineering project that builds a complete, production-ready pipeline to collect, process, validate, and visualize job data from Wuzzuf.net. The project is fully containerized using Docker and orchestrated with Apache Airflow.
![Workflow](Images/Workflow.jpg)

## 🚀 Overview

**WuzzufFlow** is a fully automated, Dockerized data pipeline designed to scrape job listings from [Wuzzuf](https://wuzzuf.net), process and validate the data, store it in a PostgreSQL database, and visualize it via an interactive Streamlit dashboard.

The project demonstrates real-world Data Engineering skills using modern open-source technologies such as:

- **Web Scraping** with `BeautifulSoup`
- **HDFS** for distributed storage
- **Apache Spark** for large-scale data transformation
- **Great Expectations** for data validation
- **PostgreSQL** for structured data storage
- **Streamlit** and `Plotly` for live dashboards
- **Apache Airflow** for orchestration and scheduling
- **Docker Compose** for environment management

---

## 🛠️ Tech Stack

| Task             | Tool/Technology             |
|------------------|-----------------------------|
| Web Scraping     | `BeautifulSoup`, `requests` |
| Storage Layer    | `HDFS`                      |
| Processing       | `Apache Spark`, `PySpark`   |
| Validation       | `Great Expectations`        |
| Database         | `PostgreSQL`                |
| Dashboard        | `Streamlit`, `Plotly`       |
| Orchestration    | `Apache Airflow`            |
| Containerization | `Docker Compose`            |

---

## 📂 Project Structure

