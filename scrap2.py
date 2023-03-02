from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

jobs = ['Data Analyst', 'Analytics Engineer']
locations = ['Amsterdam', 'Berlin','Barcelona']

job_data = []

for job in jobs:
    for location in locations:
        job_name = job
        country_name = location

        job_url = "";
        for item in job_name.split(" "):
            if item != job_name.split(" ")[-1]:
                job_url = job_url + item + "%20"
            else:
                job_url = job_url + item

        country_url = "";
        for item in country_name.split(" "):
            if item != country_name.split(" ")[-1]:
                country_url = country_url + item + "%20"
            else:
                country_url = country_url + item

        geoId = ""
        if "Amsterdam" in country_url:
            geoId = "103100785"
        elif "Berlin" in country_url:
            geoId = "104857295"
        elif "Barcelona" in country_url:
            geoId = "105149172"
#        elif "Amsterdam" in country_url:
#            geoId = "103100785"


        url = "https://www.linkedin.com/jobs/{0}-jobs-{1}?keywords={2}&location={3}&locationId=&geoId={4}&f_TPR=r86400&distance=25&position=1&pageNum=0".format(job_name.lower().replace(" ", "-"), country_name.lower().replace(" ", "-"), job_url, country_url, geoId)

        # Creating a webdriver instance
        browser = webdriver.Firefox()

        # Opening the url we have just defined in our browser
        browser.get(url)