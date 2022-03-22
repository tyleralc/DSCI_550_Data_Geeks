from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# function to take care of downloading file
def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

# instantiate a chrome options object so you can set the size and headless preference
# some of these chrome options might be uncessary but I just used a boilerplate
# change the <path_to_download_default_directory> to whatever your default download folder is located
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "<path_to_download_default_directory>",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
})
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')

# initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
ser = Service(r"C:\Users\Tyler Alcorn\OneDrive - University of Southern California\Documents\GitHub\DSCI_550_Data_Geeks\HW2\chromedriver.exe")
driver = webdriver.Chrome(options=chrome_options, service=ser)

# change the <path_to_place_downloaded_file> to your directory where you would like to place the downloaded file
download_dir = r"C:\Users\Tyler Alcorn\OneDrive - University of Southern California\Documents\GitHub\DSCI_550_Data_Geeks\HW2\pdfs"

# function to handle setting up headless download
enable_download_headless(driver, download_dir)

# get request to target the site selenium is active on
#driver.get(f"https://libraries.usc.edu/search/all?query={DOI}")
driver.get("https://libraries.usc.edu/search/all?query=10.1371/journal.pone.0053510")
# initialize an object to the location on the html page and click on it to download
#find_element_by_css_selector is deprecated. Please use find_element(by=By.CSS_SELECTOR, value=css_selector)
search_input = driver.find_element(by=By.CSS_SELECTOR, value='#Articles > div > div > ul > li:nth-child(1) > article > div.search-bento-item__content > div.flex > div.links > a > span.dl-article')
search_input.click()