from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import ElementNotVisibleException , StaleElementReferenceException ;
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
import time


import os
import sys



chrome_options = Options()
s = Service('/usr/local/bin/chromedriver')
print("A")
chrome_options.add_argument("--headless")
chrome_options.add_argument('window-size=1920x1280')
print("B")
driver = webdriver.Chrome(service=s,options=chrome_options)
actions = ActionChains(driver)
print("C")
wait = WebDriverWait(driver, 2000)
print("D")
driver.get("https://www.vattenfall.se/elavtal/elpriser/timpris/#setimpris")
#print("E")
wait.until( EC.visibility_of_element_located((By.ID, "cmpbntyestxt"))).click()
print("CLICKED ACCEPT")
e = wait.until( EC.visibility_of_element_located((By.XPATH, "//label[text()='Välj period']")))
#driver.execute_script("window.scrollTo(100,document.body.scrollHeight);")
#print(f"LOCATION = {e.location['y']}")
#ys = e.location['y'] - 400
#ys = 2138
#script = f"window.scrollTo(100,{ys})"
#print(f"script = {script}")
#driver.execute_script(f"window.scrollTo(100,{ys})")
e = e.find_element("xpath","./..")
e = e.find_element("xpath",".//div")
print("OK1")
#print(f"e = {e.get_attribute('innerHTML')}")
e.find_element("xpath","./button").click()
print("OK2")
e2 = e.find_element("xpath","//a[text()='En vecka framåt (per timme)']")
print("OK2.5")
e2.click()
#drops = driver.find_elements(By.CLASS_NAME,"dropdown-toggle")
#i = 0
#for drop in drops:
#    print(f"#######")
#    p = drop.find_element("xpath",'./..')
#    print(f" I = {i} \n {p.get_attribute('value')}")
#    if i == 1 :
#        p.click()
#    i  = i + 1 
#time.sleep(2)
#e2.click()
print("OK3")
e5 = wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "hourlyspotpriceblock")))
#wait.until( EC.element_to_be_clickable((By.XPATH, "//button//span[@class='icon.icon-down'"))).click()
print("OK4")

#print(f" {e5.get_attribute('innerHTML')}")
#wait.until( EC.visibility_of_element_located((By.XPATH, "//a[text()='wait forever'")))
cells = driver.find_elements(By.CLASS_NAME,"ui-grid-cell-contents")
for cell in cells :
    print(f"{cell.get_attribute('innerHTML')}")
#wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "forever")))
#print(f"FOUND LOGIN")
#print(f"LOOK FOR USERNAME")
#username_box = driver.find_element(By.NAME,'username')
#username_box.send_keys(USERNAME)
#password_box = driver.find_element(By.NAME,'password')
#password_box.send_keys(PASSWORD)
#print(f"LOOK FOR btn.btn-info")
#wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "btn.btn-info.btn-sm"))).click()
#print(f"WAIT FOR THERMIA")
#wait.until( EC.visibility_of_element_located((By.ID, "THERMIA"))).click()
#print(f"WAIT FOR THERMIA MENU")
#wait.until( EC.visibility_of_element_located((By.ID, "THERMIA_MENU"))).click()
#print(f"B")
#i = 0
#done = False
#while i < 3 and not done  :
#    try :
#        print(f" iteration = {i}")
#        i = i + 1
#        driver.refresh();
#        wait.until( EC.element_to_be_clickable((By.ID, "RUM_BOR2_d"))).click()
#        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "form-control.input-sm"))).clear()
#        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "form-control.input-sm"))).send_keys(RUM_BOR2_d)
#        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "glyphicon.glyphicon-ok"))).click()
#        print(f"E")
#        
#        driver.refresh();
#        wait.until( EC.element_to_be_clickable((By.ID, "VV_START_d"))).click()
#        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "form-control.input-sm"))).clear()
#        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "form-control.input-sm"))).send_keys(VV_START_d)
#        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "glyphicon.glyphicon-ok"))).click()
#        print(f"F")
#        
#        driver.refresh();
#        wait.until( EC.element_to_be_clickable((By.ID, "VV_STOP_d"))).click()
#        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "form-control.input-sm"))).clear()
#        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "form-control.input-sm"))).send_keys(VV_STOP_d)
#        wait.until( EC.visibility_of_element_located((By.CLASS_NAME, "glyphicon.glyphicon-ok"))).click()
#        print(f"G")
#        done = True
#    except StaleElementReferenceException as e :
#        print(f"ERROR {type(e).__name__}")
#    
#
#
#
driver.close()
