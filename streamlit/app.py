import pandas as pd
import psycopg2
import streamlit as st
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from wordcloud import WordCloud
import matplotlib.pyplot as plt

DB_HOST = "postgres"  
DB_PORT = "5432"
DB_NAME = "job_data"
DB_USER = "airflow"
DB_PASS = "airflow"

@st.cache_data(ttl=60)
def get_data(query):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df


st.set_page_config(page_title="Job Dashboard", layout="wide")

html_temp = """
            <div style="background-color:tomato;padding:10px">
            <h1 style="color:white;text-align:center"> 💼 Job Market Dashboard</h1>
            </div>
                   """
st.markdown(html_temp,unsafe_allow_html=True)

st.subheader("Latest Job Data")
report = get_data("SELECT job_title,work_type,workplace,company_name,company_page,experience_level,yrs_of_exp,address,city,country " \
                  "FROM jobs WHERE job_title ILIKE '%data%'"\
                  "ORDER BY RANDOM()"\
                  "limit 10")
st.dataframe(report)

col1,col2,col3=st.columns(3)
with col1:

        report=get_data('select experience_level , count(*) as "Jobs" ' \
        '                from jobs ' \
        '                group by experience_level ' \
        '                order by count(*) desc ')

        fig=px.bar(data_frame=report,
                   x="experience_level",
                   y="Jobs",
                   color="experience_level",
                   text="Jobs",
                   title="#Jobs for each Experience level",
        )
        st.plotly_chart(fig,use_container_width=True)


with col2:

        report=get_data('select work_type , count(*) as "Jobs" ' \
        '                from jobs ' \
        '                where work_type != \'Hybrid\' and work_type != \'On-site\' ' \
        '                group by work_type ' \
        '                order by count(*) desc')

        fig=px.bar(data_frame=report,
                   x="work_type",
                   y="Jobs",
                   color="work_type",
                   text="Jobs",
                   title="#Jobs for each Work type",
        )
        st.plotly_chart(fig,use_container_width=True)

with col3:

        report=get_data('select workplace , count(*) as "Jobs" ' \
        'from jobs ' \
        'where workplace != \'Part Time\' and  workplace != \'Internship\'  ' \
        'group by workplace ' \
        'order by count(*) desc')

        fig=px.bar(data_frame=report,
                   x="workplace",
                   y="Jobs",
                   color="workplace",
                   text="Jobs",
                   title="#Jobs for each workplace ",
        )
        st.plotly_chart(fig,use_container_width=True)

col1,col2=st.columns(2)
with col1:

        report=get_data('select country,count(*) as "Jobs" from Jobs group by country order by count(*) Desc limit 10')
        fig=px.bar(data_frame=report,
                   x="country",
                   y="Jobs",
                   color="country",
                   text="Jobs",
                   title="#Jobs for each Country",
        )
        st.plotly_chart(fig,use_container_width=True)

with col2:

        report=get_data('select city,count(*) as "Jobs" from Jobs group by city order by count(*) Desc limit 10')
        fig=px.bar(data_frame=report,
                   x="city",
                   y="Jobs",
                   color="city",
                   text="Jobs",
                   title="#Jobs for each City",
        )
        st.plotly_chart(fig,use_container_width=True)


df = get_data("SELECT s.skills  FROM skills s INNER JOIN jobs j ON s.job_id = j.id WHERE j.job_title ILIKE '%data%';")
text = " ".join(df["skills"].dropna().astype(str))

wordcloud = WordCloud(width=800, height=300, background_color='white').generate(text)
st.subheader("Top Skills")
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

st_autorefresh(interval=300000, key="job_autorefresh")
