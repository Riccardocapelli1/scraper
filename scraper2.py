# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# Define job and location prompts to search
#jobs_prompt = ['dbt','SSIS','Analytics Engineer','Data Analyst']
#locations = ['Amsterdam','Berlino','Barcellona']

# Define job and location prompts to search
jobs_prompt = ['Analisi dei Dati','Vendite']
locations = ['Reggio','Verona']

# Loop through each job and location
for job in jobs_prompt:
    for location in locations:
        job_name = job
        country_name = location
        
        # Define filename to save results to
        filename = f"{job_name.lower().replace(' ', '-')}_{country_name.lower().replace(' ', '-')}_{time.strftime('%d-%m-%Y')}.csv"

        # Create URL to search for jobs
        job_url = ""
        for item in job_name.split(" "):
            if item != job_name.split(" ")[-1]:
                job_url = job_url + item + "%20"
            else:
                job_url = job_url + item
        country_url = ""
        for item in country_name.split(" "):
            if item != country_name.split(" ")[-1]:
                country_url = country_url + item + "%20"
            else:
                country_url = country_url + item

        # Assign a geoId to the country based on location
        geoId = ""
        if "Amsterdam" in country_url:
            geoId = "103100785"
        elif "Berlin" in country_url:
            geoId = "106967730"
        elif "Barcelona" in country_url:
            geoId = "107025191"
        elif "Reggio" in country_url:
            geoId = "102687173"
        elif "Verona" in country_url:
            geoId = "102557975"   

        # Define the URL with job and location information
        url = "https://www.linkedin.com/jobs/{0}-jobs-{1}?keywords={2}&location={3}&locationId=&geoId={4}&f_TPR=r86400&distance=25&position=1&pageNum=0".format(job_name.lower().replace(" ", "-"), country_name.lower().replace(" ", "-"), job_url, country_url, geoId)

        # Create a webdriver instance
        browser = webdriver.Firefox()

        # Open the URL in the browser
        browser.get(url)

        # Find the number of jobs available
        jobs_num = browser.find_element(By.CSS_SELECTOR,"h1>span").get_attribute("innerText")
        if len(jobs_num.split(',')) > 1:
            jobs_num = int(jobs_num.split(',')[0])*1000
        else:
            jobs_num = int(jobs_num)
        jobs_num   = int(jobs_num)

        # Scroll down to the end of the page to load all job postings
        i = 2
        while i <= int(jobs_num/2)+1:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            i = i + 1
            print("Current at: ", i, "Percentage at: ", ((i+1)/(int(jobs_num/2)+1))*100, "%",end="\r")
            try:
                # If there is a "Load more results" button, click it
                infinite_scroller_button = browser.find_element(By.XPATH, ".//button[@aria-label='Load more results']")
                infinite_scroller_button.click()
                time.sleep(0.1)
            except:
                # If there is no "Load more results" button, just keep scrolling down
                time.sleep(0.1)
                pass

        #We get a list containing all jobs that we have found.
        job_lists = browser.find_element(By.CLASS_NAME,"jobs-search__results-list")
        jobs_tags = job_lists.find_elements(By.TAG_NAME,"li") # return a list

        #We declare void list to keep track of all obtaind data.
        job_title_list = []
        company_name_list = []
        location_list = []
        date_list = []
        job_link_list = []
        
        #We loof over every job_element and obtain all the wanted info.
        for job_element in jobs_tags:
            #job_title
            job_title = job_element.find_element(By.CSS_SELECTOR,"h3").get_attribute("innerText")
            job_title_list.append(job_title)
            
            #company_name
            company_name = job_element.find_element(By.CSS_SELECTOR,"h4").get_attribute("innerText")
            company_name_list.append(company_name)
            
            #location
            location = job_element.find_element(By.CSS_SELECTOR,"div>div>span").get_attribute("innerText")
            location_list.append(location)
            
            #date
            date = job_element.find_element(By.CSS_SELECTOR,"div>div>time").get_attribute("datetime")
            date_list.append(date)
            
            #job_link
            job_link = job_element.find_element(By.CSS_SELECTOR,"a").get_attribute("href")
            job_link_list.append(job_link)

        jd = [] #job_description
        seniority = []
        emp_type = []
        job_func = []
        job_ind = []
        for item in range(len(jobs_tags)):
            print(item)
            job_func0=[]
            industries0=[]
            # clicking job_element to view job_element details
            
            #__________________________________________________________________________ job_element Link
            
            try: 
                job_click_path = f'/html/body/div/div/main/section/ul/li[{item+1}]'
                job_click = job_element.find_element(By.XPATH,job_click_path).click()
            except:
                pass
            #job_click = job_element.find_element(By.XPATH,'.//a[@class="base-card_full-link"]')
            
            #__________________________________________________________________________ job_element Description
            jd_path = '/html/body/div/div/section/div/div/section/div/div/section/div'
            try:
                jd0 = job_element.find_element(By.XPATH,jd_path).get_attribute('innerText')
                jd.append(jd0)
            except:
                jd.append(None)
                pass
            
            #__________________________________________________________________________ job_element Seniority
            seniority_path='/html/body/div/div/section/div/div/section/div/ul/li[1]/span'
            
            try:
                seniority0 = job_element.find_element(By.XPATH,seniority_path).get_attribute('innerText')
                seniority.append(seniority0)
            except:
                seniority.append(None)
                pass

            #__________________________________________________________________________ job_element Time
            emp_type_path='/html/body/div/div/section/div/div/section/div/ul/li[2]/span'
            
            try:
                emp_type0 = job_element.find_element(By.XPATH,emp_type_path).get_attribute('innerText')
                emp_type.append(emp_type0)
            except:
                emp_type.append(None)
                pass
            
            #__________________________________________________________________________ job_element Function
            function_path='/html/body/div/div/section/div/div/section/div/ul/li[3]/span'
            
            try:
                func0 = job_element.find_element(By.XPATH,function_path).get_attribute('innerText')
                job_func.append(func0)
            except:
                job_func.append(None)
                pass

            #__________________________________________________________________________ job_element Industry
            industry_path='/html/body/div/div/section/div/div/section/div/ul/li[4]/span'
            
            try:
                ind0 = job_element.find_element(By.XPATH,industry_path).get_attribute('innerText')
                job_ind.append(ind0)
            except:
                job_ind.append(None)
                pass
            
            print("Current at: ", item, "Percentage at: ", (item+1)/len(jobs_tags)*100, "%")

            #close the browser
            browser.quit()
            
            job_data = pd.DataFrame({
                'Date': date,
                'Company': company_name,
                'Title': job_title,
                'Location': location,
                'Description': jd,
                'Level': seniority,
                'Type': emp_type,
                'Function': job_func,
                'Industry': job_ind,
                'Link': job_link
            })

            job_data_print = job_data.append(job_data)
            
            # save the dataframe to csv
            job_data_print.to_csv(filename, index=False)