from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import ElementNotVisibleException , StaleElementReferenceException ;


import os
import sys


#RUM_BOR2_d = '23'
#VV_START_d = '42'
#VV_STOP_d = '55'

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')


[script,RUM_BOR2_d,VV_START_d,VV_STOP_d] = sys.argv

print(f"{RUM_BOR2_d} {VV_START_d} {VV_STOP_d}")
chrome_options = Options()
s = Service('/usr/local/bin/chromedriver')
print("A")
chrome_options.add_argument("--headless")
chrome_options.add_argument('window-size=1920x1080')
print("B")
driver = webdriver.Chrome(service=s,options=chrome_options)
print("C")
wait = WebDriverWait(driver, 2000)
print("D")
driver.get("http://localhost:8888")
print("E")
c = wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "caret"))).click()
print(f"FOUND LOGIN")
print(f"LOOK FOR USERNAME")
username_box = driver.find_element(By.NAME,'username')
username_box.send_keys(USERNAME)
password_box = driver.find_element(By.NAME,'password')
password_box.send_keys(PASSWORD)
print(f"LOOK FOR btn.btn-info")
wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "btn.btn-info.btn-sm"))).click()
print(f"WAIT FOR THERMIA")
wait.until( EC.visibility_of_element_located((By.ID, "THERMIA"))).click()
print(f"WAIT FOR THERMIA MENU")
wait.until( EC.visibility_of_element_located((By.ID, "THERMIA_MENU"))).click()
print(f"B")
i = 0
done = False
while i < 3 and not done  :
    try :
        print(f" iteration = {i}")
        i = i + 1
        driver.refresh();
        wait.until( EC.element_to_be_clickable((By.ID, "RUM_BOR2_d"))).click()
        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "form-control.input-sm"))).clear()
        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "form-control.input-sm"))).send_keys(RUM_BOR2_d)
        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "glyphicon.glyphicon-ok"))).click()
        print(f"E")
        
        driver.refresh();
        wait.until( EC.element_to_be_clickable((By.ID, "VV_START_d"))).click()
        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "form-control.input-sm"))).clear()
        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "form-control.input-sm"))).send_keys(VV_START_d)
        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "glyphicon.glyphicon-ok"))).click()
        print(f"F")
        
        driver.refresh();
        wait.until( EC.element_to_be_clickable((By.ID, "VV_STOP_d"))).click()
        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "form-control.input-sm"))).clear()
        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "form-control.input-sm"))).send_keys(VV_STOP_d)
        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "glyphicon.glyphicon-ok"))).click()
        print(f"G")
        done = True
    except StaleElementReferenceException as e :
        print(f"ERROR {type(e).__name__}")
    



driver.close()
