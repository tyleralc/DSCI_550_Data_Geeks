ReadMe for pdf_download.py

Requirements 
-------------------------------------------------------------------------
All libraries used are as follows:
-from selenium import webdriver
-from selenium.webdriver.chrome.options import Options
-from selenium.webdriver.chrome.service import Service
-from selenium.webdriver.common.by import By
-from selenium.webdriver.support.ui import WebDriverWait
-from selenium.webdriver.support import expected_conditions as EC
-from selenium.webdriver.common.keys import Keys
-import pandas as pd
-import time
-import os

Installed chromedriver.exe file for the chrome browser version on the computer being used. The path must to known, will be asked for later

How to run the code: 
-------------------------------------------------------------------------
1) First, at line 20 put in the path of the download directory desired for the files to go into. 

2) At line 35, insert the path to the chromredriver.exe file. 

3) At line 49, enter your USC login username, in the send_keys() method, comment on the line above explains further.

4) At line 51, enter your USC login password, in the send_keys() method, comment on the line above explains further.

5)At line 84 and 85, rename the paths to the download directory selected, with line 84, including \file.pdf at the end of the path to rename all the files that will be named file.pdf when downloaded. 

6) Run the file from the command line as follows: python3 pdf_download.py

7) After running a file, a chrome browser will begin running and requires the user, if using the USC login, must go in and click the two factor authorization option of their choice and follow the direction to complete that 2 factor authentication. Then, the files will begin downloading files and renaming as mentioned in the code. 

8)The program should then run and give updates of the status of each download 


Results:
-------------------------------------------------------------------------
Pdf files will be downloaded to the desired download directory. File names will vary due to the multiple names assigned by the websites used to download the files. 
