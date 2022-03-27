from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# function to take care of downloading file
def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

# instantiate a chrome options object so you can set the size and headless preference
# some of these chrome options might be uncessary but I just used a boilerplate
# change the <path_to_download_default_directory> to whatever your default download folder is located
chrome_options = Options()

# header = {'User-Agent': 'Chrome/97.0.4692.71'}
# response = requests.get(url,headers=header)

download_dir = r"C:\Users\Tyler Alcorn\OneDrive - University of Southern California\Documents\GitHub\DSCI_550_Data_Geeks\HW2\pdfs"
#testing if needed 
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")
# chrome_options.add_argument("--disable-notifications")
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False,
        "plugins.always_open_pdf_externally": True
})
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--disable-software-rasterizer')
chrome_options.add_argument('--log-level=1')
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])


# initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
ser = Service(r"C:\Users\Tyler Alcorn\OneDrive - University of Southern California\Documents\GitHub\DSCI_550_Data_Geeks\HW2\chromedriver.exe")
driver = webdriver.Chrome(options=chrome_options, service=ser)

# change the <path_to_place_downloaded_file> to your directory where you would like to place the downloaded file
download_dir = r"C:\Users\Tyler Alcorn\OneDrive - University of Southern California\Documents\GitHub\DSCI_550_Data_Geeks\HW2\pdfs"

# function to handle setting up headless download
enable_download_headless(driver, download_dir)

#get the list of DOIs from final bik dataset

df = pd.read_csv("Final_bik_dataset.tsv", sep='\t', encoding = "ISO-8859-1")
doi= df["DOI"].tolist()
first5_doi=doi[0:4]

# get request to target the site selenium is active on
#driver.get(f"https://libraries.usc.edu/search/all?query={DOI}")

#below was single test
#10.1371/journal.pone.0053940
#driver.get("https://libraries.usc.edu/search/all?query=10.1371/journal.pone.0053940")

# initialize an object to the location on the html page and click on it to download
#find_element_by_css_selector is deprecated. Please use find_element(by=By.CSS_SELECTOR, value=css_selector)

#below was single test
#search_input=driver.find_element(by=By.CLASS_NAME, value='isvg loaded')
#search_input =driver.find_element(by=By.XPATH, value="//span[@class='dl-article']")
#search_input =driver.find_element(by=By.CSS_SELECTOR, value='.dl-article')
#search_input=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".dl-article"))).click()

#obtain window handle of browser in focus
# p = driver.current_window_handle
# #obtain parent window handle
# parent = driver.window_handles[0]
# #obtain browser tab window
# chld = driver.window_handles[1]
# #switch to browser tab
# driver.switch_to.window(chld)

#search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located("#Articles > div > div > ul > li > article > div.search-bento-item__content > div.flex > div.links > a > span.dl-article"))
#search_input = driver.find_element(by=By.CSS_SELECTOR, value='#Articles > div > div > ul > li:nth-child(1) > article > div.search-bento-item__content > div.flex > div.links > a > span.dl-article')
# search_input.click()
# time.sleep(2)
# <span class="dl-article">Download PDF</span>
more_results='#Articles > div > div > ul > li:nth-child(1) > article > div.search-bento-item__content > div.flex > div.links > a > span.dl-article'      #more than one result in the search 
one_result='#Articles > div > div > ul > li > article > div.search-bento-item__content > div.flex > div.links > a > span.dl-article'                  #one result

def get_pdfs(DOI):
    try:
        driver.get(f"https://libraries.usc.edu/search/all?query={DOI}")
        search_input=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".dl-article"))).click()
        
    except: #NoSuchElementException:
        print('failed')


def tiny_file_rename(newname, folder_of_download, time_to_wait=60):
    time_counter = 0
    filename = max([f for f in os.listdir(folder_of_download)], key=lambda xa:os.path.getctime(os.path.join(folder_of_download,xa)))
    while '.part' in filename:
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:
            raise Exception('Waited too long for file to download')
    filename = max([f for f in os.listdir(folder_of_download)], key=lambda xa :   os.path.getctime(os.path.join(folder_of_download,xa)))
    os.rename(os.path.join(folder_of_download, filename), os.path.join(folder_of_download, newname))


for i in first5_doi:
    get_pdfs(first5_doi)
    time.sleep(15)
    old_name= r'C:\Users\Tyler Alcorn\OneDrive - University of Southern California\Documents\GitHub\DSCI_550_Data_Geeks\HW2\pdfs\file.pdf'
    new_path= r'C:\Users\Tyler Alcorn\OneDrive - University of Southern California\Documents\GitHub\DSCI_550_Data_Geeks\HW2\pdfs\ '
    file_name= str(i)
    new_name =new_path+file_name
    os.rename(old_name, new_name)
    #tiny_file_rename(str(i)+'.pdf', download_dir, time_to_wait=60)
    doi_index_number = doi.index(i) + 1
    doi_length = str(len(doi))
    print(f"{doi_index_number} out of {doi_length}")

print(first5_doi)

