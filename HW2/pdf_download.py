from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import os

#function to create the headless browser
def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)
#sets up the chrome options 
chrome_options = Options()
##place your download 
download_dir = r"C:\Users\Tyler Alcorn\OneDrive - University of Southern California\Documents\GitHub\DSCI_550_Data_Geeks\HW2\pdfs"

#adjusts all the settings on the chrome browser and moves the download directory to the user desired folder 
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

#service is the location of the chromedriver.exe file, this must be changed to the location of the user's chromedriver
ser = Service(r"C:\Users\Tyler Alcorn\OneDrive - University of Southern California\Documents\GitHub\DSCI_550_Data_Geeks\HW2\chromedriver.exe")

#this sets up the driver to a variable that will be used to navigate to websites
driver = webdriver.Chrome(options=chrome_options, service=ser)

#enables the chrome browser to open
enable_download_headless(driver, download_dir)

##navigates the browser to USC library and sets up the login to the USC account
##not required to get most files, but several pdfs require a USC login to download ##
#this group of code(46-54) may be commented out if USC login is not wanted or possible
driver.get("https://libraries.usc.edu")
driver.find_element(By.CSS_SELECTOR, ".site-header__signin").click()
##enter USC username in the send_keys(___), ensure username is a string 
driver.find_element(By.CSS_SELECTOR, "#username").send_keys("/username/")
##enter USC password to sign into your USC account by placing password in send_keys(___), ensure password is a string 
driver.find_element(By.CSS_SELECTOR, "#password").send_keys("/password/")
driver.find_element(By.CSS_SELECTOR, "#password").send_keys(Keys.ENTER)
###once the screen pops up click the method of 2 factor authorization preferred, amd verify the method used. There is a 15 sec time frame for this action to be completed. 
time.sleep(15)

#function to get pdfs           
def get_pdfs(DOI, title):
    #first it attempts to find the pdf by searching the doi 
    try:
        driver.get(f"https://libraries.usc.edu/search/all?query={DOI}")
        search_input=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".dl-article"))).click()
    #if no links come up from that search, then it searches by the title 
    except:
        try:
            driver.get(f"https://libraries.usc.edu")
            driver.find_element(By.CSS_SELECTOR, "#edit-search").send_keys(title)
            driver.find_element(By.CSS_SELECTOR, "#edit-search").send_keys(Keys.ENTER)
            search_input=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".dl-article"))).click()
        #if all attempts to search fail, then it prints out 'failed' for the user to see that it failed  
        except:
            print('failed')

#getting the lists of dois and titles 
df = pd.read_csv("Final_bik_dataset.tsv", sep='\t', encoding = "ISO-8859-1")
doi= df["DOI"].tolist()
title=df["Title"].tolist()

#for loop to go through each line o
for (i, j) in zip(doi, title):
    get_pdfs(i,j)
    time.sleep(30)
    #check if a file.pdf is present and if it is equal to the old_name then do the rename functions 
    old_name= r'C:\Users\Tyler Alcorn\OneDrive - University of Southern California\Documents\GitHub\DSCI_550_Data_Geeks\HW2\pdfs\file.pdf'
    new_path= r'C:\Users\Tyler Alcorn\OneDrive - University of Southern California\Documents\GitHub\DSCI_550_Data_Geeks\HW2\pdfs\\'

    #renames the files to a suitable name for saving purposes 
    i=i.replace('/', '_')
    try:
        #if the file downloaded is file, the name is changed here to prevent save over of the previous file named file.pdf
        file_name= '\\' +str(i)+'.pdf'
        new_name =new_path+file_name
        os.rename(old_name, new_name)
    except:
        print('not named file.pdf')
    #names the files back to the proper doi for searching on the next iteration
    i=i.replace('_', '/')
    #tracker of the process of where the program is at in the downloading process
    doi_index_number = doi.index(i) + 1
    doi_length = str(len(doi))
    print(f"{doi_index_number} out of {doi_length}")