import pandas as pd
df = pd.read_csv("Final_bik_dataset.tsv", sep='\t', encoding = "ISO-8859-1")
doi= df["DOI"].tolist()
title=df["Title"].tolist()
failed=[]
i=[51, 52, 54, 56, 57, 60, 135, 136, 138, 144, 151, 154, 155, 156, 157, 159, 160, 162, 164, 166, 168, 169, 170, 173]
for index in i:
    failed.append(title[index])

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

chrome_options = Options()

download_dir = r"C:\Users\Tyler Alcorn\OneDrive - University of Southern California\Documents\GitHub\DSCI_550_Data_Geeks\HW2\pdfs"

chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False,
        "plugins.always_open_pdf_externally": True
})

chrome_options.add_argument('--log-level=1')
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

ser = Service(r"C:\Users\Tyler Alcorn\OneDrive - University of Southern California\Documents\GitHub\DSCI_550_Data_Geeks\HW2\chromedriver.exe")
driver = webdriver.Chrome(options=chrome_options, service=ser)

enable_download_headless(driver, download_dir)

driver.get(f"https://libraries.usc.edu")
driver.find_element(By.CSS_SELECTOR, "#edit-search").send_keys('Hemin-Induced Modifications of the Antigenicity and Hemin-Binding Capacity of Porphyromonas gingivalis Lipopolysaccharide')
driver.find_element(By.CSS_SELECTOR, "#edit-search").send_keys(Keys.ENTER)
search_input=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".dl-article"))).click()
            






def get_pdfs(DOI, title):
    try:
        driver.get(f"https://libraries.usc.edu/search/all?query={DOI}")
        search_input=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".dl-article"))).click()
        
    except: #NoSuchElementException:
        try:
            driver.get(f"https://libraries.usc.edu")
            driver.find_element(By.CSS_SELECTOR, "#edit-search").send_keys('Hemin-Induced Modifications of the Antigenicity and Hemin-Binding Capacity of Porphyromonas gingivalis Lipopolysaccharide')
            driver.find_element(By.CSS_SELECTOR, "#edit-search").send_keys(Keys.ENTER)
            search_input=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".dl-article"))).click()
            
        except:
            print('failed')

test_doi=doi[50:54]
test_title=title[50:54]

for (i, j) in zip(doi, title):
    get_pdfs(i,j)
    time.sleep(5)
    #check if a file.pdf is present and if it is equal to the old_name then do the rename functions 
    old_name= r'C:\Users\Tyler Alcorn\OneDrive - University of Southern California\Documents\GitHub\DSCI_550_Data_Geeks\HW2\pdfs\file.pdf'
    new_path= r'C:\Users\Tyler Alcorn\OneDrive - University of Southern California\Documents\GitHub\DSCI_550_Data_Geeks\HW2\pdfs'

    i=i.replace('/', '_')
    try:
        
        file_name= '\\' +str(i)+'.pdf'
        new_name =new_path+file_name
        os.rename(old_name, new_name)
        
    except:
        print('not name file.pdf')
    i=i.replace('_', '/')
    doi_index_number = doi.index(i) + 1
    doi_length = str(len(doi))
    print(f"{doi_index_number} out of {doi_length}")