# import pandas as pd
# df = pd.read_csv("Final_bik_dataset.tsv", sep='\t', encoding = "ISO-8859-1")
# doi= df["DOI"].tolist()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager


def download_file(DOI):                    #(file_path, DOI):
    #object of ChromeOptions class
    op = webdriver.ChromeOptions()
    #op.add_extension('Adblock-Plus_v1.4.1.crx')
    #browser preferences
    p = {"download.default_directory":"Desktop\\Downloads"}
    
    #"C:\\Users\\Tyler Alcorn\\OneDrive - University of Southern California\\Documents\\GitHub\\DSCI_550_Data_Geeks\\HW2\\pdfs"}

    #add options to browser
    op.add_experimental_option('prefs', p)

    #set chromedriver.exe path
    #driver = webdriver.Chrome(executable_path="C:\\chromedriver.exe", options=op)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #maximize browser
    driver.maximize_window()
    #launch URL
    driver.get(f"https://libraries.usc.edu/search/all?query={DOI}");
    #click download link
    # l = driver.find_element_by_link_text("dl-article")
    # l.click() 
    search_input = driver.find_element_by_css_selector('#Articles > div > div > ul > li:nth-child(1) > article > div.search-bento-item__content > div.flex > div.links > a > span:nth-child(2)')
    search_input.click()


# try:

#     driver.get('https://www.browserstack.com/test-on-the-right-mobile-devices');

#     downloadcsv= driver.find_element_by_css_selector('.icon-csv');

#     gotit= driver.find_element_by_id('accept-cookie-notification');

#     gotit.click();    

#     downloadcsv.click();

#     time.sleep(5)

#     driver.close()

# except:

#      print("Invalid URL")


if __name__=="__main__":
    download_file('10.1371/journal.pone.0053510')