# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 23:25:29 2019

@author: Aisha Alabdullatif
"""


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait as wdw
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd
from time import sleep
from datetime import datetime

# Setting up browser driver
driver = webdriver.Chrome()

# Prompt for details
keywords = input('Search keywords (this can be null): ')
sloc = input('Job Location (this can be null, default is Saudi Arabia): ')

# Process recieved text for URL
if sloc == '':
    sloc = 'Saudi%20Arabia'
else:
    sloc = sloc.replace(' ' or '\n','%20')
keywords = keywords.replace(' ' or '\n','%20')

# Redirect to job posting page
driver.get('https://www.linkedin.com/jobs/search?keywords='+keywords+'&location='+sloc+'&geoId=&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0')

# Dictionary setup to hold scraped data
jobs = {'URL': [],
        'Title': [],
        'Company': [],
        'Location': [],
        'Since': []
        }

# Allow 5 sec for the page to load
sleep(5)

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    sleep(1)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Limit more button click count based on Linkedin terms
more_ct = 0
while True and more_ct < 5:
    more_button = driver.find_elements_by_xpath('//*[@id="main-content"]/div/section/button')[0]
    more_button.click()
    more_ct += 1

# Begin saving job details
for i in range(1,1001):
    try:
        # Collect data
        url = driver.find_element_by_xpath('/html/body/main/div/section/ul/li['+str(i)+']/a').get_attribute('href').strip()
        title = driver.find_element_by_xpath('/html/body/main/div/section/ul/li['+str(i)+']/div[1]/h3').text.encode('utf-8').strip()
        company = driver.find_element_by_xpath('/html/body/main/div/section/ul/li['+str(i)+']/div[1]/h4/a').text.encode('utf-8').strip()
        location = driver.find_element_by_xpath('/html/body/main/div/section/ul/li['+str(i)+']/div[1]/div/span').text.encode('utf-8').strip()
        since = driver.find_element_by_xpath('/html/body/main/div/section/ul/li['+str(i)+']/div[1]/div/time').get_attribute("datetime")
        
        # Append data to jobs dictionary
        jobs['URL'].append(url)
        jobs['Title'].append(str(title,'utf-8'))
        jobs['Company'].append(str(company,'utf-8'))
        jobs['Location'].append(str(location,'utf-8'))
        jobs['Since'].append(since)

    except:
        continue

jobs_df = pd.DataFrame.from_dict(jobs)
jobs_df.to_csv('LinkedIn_jobs_'+datetime.today().strftime('%m-%d-%Y_%H-%M-%S')+'.csv')