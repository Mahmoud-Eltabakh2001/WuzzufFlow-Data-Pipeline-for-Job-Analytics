# scrape_wuzzuf.py
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

def scrape_wuzzuf():
    url = "https://wuzzuf.net/search/jobs/?q=Data&a=navbl"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        num_jobs = int(soup.find_all("strong")[0].text.replace(",", ""))
        num_pages = int(np.ceil(num_jobs / 15))

        df = pd.DataFrame([], columns=["job_title", "company_name", "company_page", 
                                       "location", "job_type", "Experience Level", 
                                       "Yrs of Exp", "skills"])
        idx = -1

        for i in range(num_pages):
            url = f"https://wuzzuf.net/search/jobs/?a=navbl&q=Data&start={i}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            Containers = soup.find_all("div", {"class": "css-1gatmva e1v1l3u10"})

            for container in Containers:
                try:
                    job_title = container.find("h2", class_="css-m604qf").text.strip()
                    company_tag = container.find("a", class_="css-17s97q8")
                    company_name = company_tag.text.strip()
                    company_page = company_tag.get("href")
                    location = container.find("span", class_="css-5wys0k").text.strip()

                    job_type1 = container.find_all("span", class_="css-1ve4b75 eoyjyou0")[0].text.strip()
                    job_type2 = container.find_all("span", class_="css-1ve4b75 eoyjyou0")[-1].text.strip()
                    try:
                        job_type3 = container.find_all("span", class_="css-o1vzmt eoyjyou0")[0].text.strip()
                        job_type = " / ".join(sorted(set([job_type1, job_type2, job_type3])))
                    except:
                        job_type = " / ".join(sorted(set([job_type1, job_type2])))

                    try:
                        div = container.find_all("div", {"class": "css-y4udm8"})[0].contents[2].text.split("·")
                    except:
                        div = container.find_all("div", {"class": "css-y4udm8"})[0].contents[1].text.split("·")
                    div = [s.strip() for s in div]

                    experience_level = ",".join(div[0:1])
                    yrs_of_exp = ",".join(div[1:2])
                    skills = div[2:]

                    idx += 1
                    df.loc[idx, "job_title"] = job_title
                    df.loc[idx, "company_name"] = company_name
                    df.loc[idx, "company_page"] = company_page
                    df.loc[idx, "location"] = location
                    df.loc[idx, "job_type"] = job_type
                    df.loc[idx, "Experience Level"] = experience_level
                    df.loc[idx, "Yrs of Exp"] = yrs_of_exp
                    df.loc[idx, "skills"] = skills

                except Exception as e:
                    print("Error parsing a job container:", e)
        
        df.to_csv("/opt/airflow/dags/Wuzzuf_data.csv", index=False)
        