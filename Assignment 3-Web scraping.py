# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 17:17:56 2025

@author: mt503
"""

'Assignment 3: Web Scraping'

"""
# %%
Task: 
    1. Choose a website of your choice that you would like to scrape data from (See some ideas
below, but this is not meant to be an exhaustive list). Use Selenium and the appropriate
web driver for your browser (e.g. Chrome, Firefox).
Write a Python script using Selenium to extract information from the website. The script
should:
- Load the website.
- Navigate to the page you want to scrape.
- Extract information from the page (e.g. text, links, images, etc.).
- Store the extracted information in a structured format, such as a pandas dataframe.
- Summarize the data, find some insights 
"""
import subprocess
import sys

try:
    import selenium
except ImportError:
  subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium'])
    
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd

# Setup the driver
serv_obj = Service('C:\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=serv_obj)

# Navigating to the Yahoo Finance website
home_url = 'https://finance.yahoo.com/'
print('Navigating to Yahoo Finance Home Page')
driver.get(home_url)

#Waiting for page to load
print('Waiting for the home page to fully load')
time.sleep(5)

#Search for 'ETFs'
search_box = driver.find_element(By.XPATH, '//*[@id="ybar-sbq"]')
search_box.send_keys('top ETFs')
search_box.submit()
print('Searching for ETFs')

#Waiting for results to load
print('Waiting for search results to fully load')
time.sleep(5)

# Click on "Top ETFs" if needed or directly go to the URL
try:
    top_etfs_link = driver.find_element(By.XPATH, '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div/nav/ul/li[7]/a/span')
    top_etfs_link.click()
    print('Navigating to the Top ETFs page...')

    # Waiting for the Top ETFs page to load
    time.sleep(5)

except Exception as e:
    print(f'Error navigating to Top ETFs page: {e}')

#Initialize a list to store all ETF data
all_etfs = []
max_pages = 6
items_per_page = 25

for page_number in range(max_pages):
    start = page_number * items_per_page
    url = f'https://finance.yahoo.com/markets/etfs/top/?start={start}&count={items_per_page}'
    print(f'Navigating to: {url}')
    driver.get(url)
    
    time.sleep(5)

#Processing ETF table rows
    try:
        rows = driver.find_elements(By.XPATH,'//tbody/tr')
        print(f'Found {len(rows)} rows of ETF data.')
    
    #Extracting data
        for row in rows:
            try:
                etf_data = {}
                #ETF Ticker
                try:
                    symbol_element = row.find_element(By.XPATH, './/td[1]/span')
                    etf_data['ETF Symbol'] = symbol_element.text
                except:
                    print(f'Unable to pull ETF Symbol')
            
                #ETF Name
                try:
                    name_element = row.find_element(By.XPATH, './/td[2]/span/div')
                    etf_data['ETF Name'] = name_element.text
                except:
                    print(f'Unable to pull ETF Name')
            
                #ETF Price
                try:
                    price_element = row.find_element(By.XPATH, './/td[4]/span/div/fin-streamer')
                    etf_data['ETF Price'] = price_element.text
                except:
                    print(f'Unable to pull ETF Price')
            
                #ETF Change
                try:
                    change_element = row.find_element(By.XPATH, './/td[5]')
                    etf_data['ETF Change'] = change_element.text
                except:
                    print(f'Unable to pull ETF Change')
            
                #ETF % Change
                try:
                    percent_change_element = row.find_element(By.XPATH, './/td[6]')
                    etf_data['ETF % Change'] = percent_change_element.text
                except:
                    print(f'Unable to pull ETF % Change')
                
                #ETF 50 Day Average
                try:
                    fifty_day_avg_element = row.find_element(By.XPATH, './/td[8]')
                    etf_data['50 Day Average'] = fifty_day_avg_element.text
                except:
                        print('Unable to pull 50 Day Average')
                
                #200 Day Average
                try:
                    two_hundred_day_avg_element = row.find_element(By.XPATH, './/td[9]')
                    etf_data['200 Day Average'] = two_hundred_day_avg_element.text
                except:
                    print('Unable to pull 200 Day Average')

                #3 Month Return
                try:
                    three_month_return_element = row.find_element(By.XPATH, './/td[10]')
                    etf_data['3 Month Return'] = three_month_return_element.text
                except:
                    print('Unable to pull 3 Month Return')

                #YTD Return
                try:
                    ytd_return_element = row.find_element(By.XPATH, './/td[11]')
                    etf_data['YTD Return'] = ytd_return_element.text
                except:
                    print('Unable to pull YTD Return')
            
                #Store the ETF entry
                all_etfs.append(etf_data)
                print(f"Added: {etf_data['ETF Name']} ({etf_data['ETF Symbol']})")
            except Exception as e:
                print(f'Error processing ETF entry: {e}')
            
    except Exception as e:
        print(f'Error finding ETF entries: {e}')
    
    try:
        next_button = driver.find_element(By.XPATH, '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div/div[2]/div[3]/button[3]')
    except:
        print(f'Error processing to the next page. Try again!')
#Create a dataframe
df = pd.DataFrame(all_etfs)     
        
#Display a summary of the data
print('\nData Summary')           
            
#Save to CSV
csv_filename = 'Top_ETFs_Dataset.csv'
df.to_csv(csv_filename, index='false')
print(f'\nData saved to {csv_filename}')   

#Close driver
driver.quit()       
            
            
            
            
            
            
            
            
            
            
            