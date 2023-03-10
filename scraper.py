from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

jobs_prompt = ['Analista Dati']
locations = ['Reggio','Verona']

job_head = []
job_detail = []

for job in jobs_prompt:
    for location in locations:
        job_name = job
        country_name = location
        filename = f"{job_name.lower().replace(' ', '-')}_{country_name.lower().replace(' ', '-')}_{time.strftime('%d-%m-%Y')}.csv"

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
            geoId = "106967730"
        elif "Barcelona" in country_url:
            geoId = "107025191"
        elif "Reggio" in country_url:
            geoId = "102687173"
        elif "Verona" in country_url:
            geoId = "90009971"   


        url = "https://www.linkedin.com/jobs/{0}-jobs-{1}?keywords={2}&location={3}&locationId=&geoId={4}&f_TPR=r86400&distance=25&position=1&pageNum=0".format(job_name.lower().replace(" ", "-"), country_name.lower().replace(" ", "-"), job_url, country_url, geoId)

        # Creating a webdriver instance
        browser = webdriver.Firefox()

        # Opening the url we have just defined in our browser
        browser.get(url)

        #We find how many jobs are offered.1000
        jobs_num = browser.find_element(By.CSS_SELECTOR,"h1>span").get_attribute("innerText")
        if len(jobs_num.split(',')) > 1:
            jobs_num = int(jobs_num.split(',')[0])*1000
        else:
            jobs_num = int(jobs_num)

        jobs_num   = int(jobs_num)

        #We create a while loop to browse all jobs. 
        i = 2
        while i <= int(jobs_num/2)+1:
            #We keep scrollind down to the end of the view.
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            i = i + 1
            print("Current at: ", i, "Percentage at: ", ((i+1)/(int(jobs_num/2)+1))*100, "%",end="\r")
            try:
                #We try to click on the load more results buttons in case it is already displayed.
                infinite_scroller_button = browser.find_element(By.XPATH, ".//button[@aria-label='Load more results']")
                infinite_scroller_button.click()
                time.sleep(0.1)
            except:
                #If there is no button, there will be an error, so we keep scrolling down.
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
        date_print = []
        company_name_print = []
        job_title_print = []
        location_print = []
        job_link_print = []
            
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

            print(job_title)
            
            date_print = date
            company_name_print = company_name
            job_title_print = job_title
            location_print = location
            job_link_print = job_link
            
                    
            job_head = pd.DataFrame({
                'Date': date_print,
                'Company': company_name_print,
                'Title': job_title_print,
                'Location': location_print,
                'Link': job_link
            })

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
        
        job_detail = pd.DataFrame({
            'Description': jd,
            'Level': seniority,
            'Type': emp_type,
            'Function': job_func,
            'Industry': job_ind
        })
        
        #close the browser
        browser.quit()
    
    # .to_csave the dataframe to csv
    job_detail.to_csv(filename, index=False)