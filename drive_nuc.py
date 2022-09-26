from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


ROOM_TARGET = '21'
WATER_START_TEMP = '40'


chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 2000)
driver.get("http://nuc2:8888")
c = wait.until( EC.presence_of_element_located((By.CLASS_NAME, "caret")))
print(f"FOUND LOGIN")
c.click()
username_box = driver.find_element(By.NAME,'username')
username_box.send_keys('uuuuu')
password_box = driver.find_element(By.NAME,'password')
password_box.send_keys('ppppp')
wait.until( EC.presence_of_element_located((By.CLASS_NAME, "btn.btn-info.btn-sm"))).click()
wait.until( EC.presence_of_element_located((By.ID, "THERMIA"))).click()
wait.until( EC.presence_of_element_located((By.ID, "THERMIA_MENU"))).click()
wait.until( EC.presence_of_element_located((By.ID, "RUM_BOR2_d"))).click()
e  = wait.until( EC.presence_of_element_located((By.CLASS_NAME, "form-control.input-sm")))
e.clear()
e.send_keys(ROOM_TARGET)
wait.until( EC.presence_of_element_located((By.CLASS_NAME, "glyphicon.glyphicon-ok"))).click()

wait.until( EC.presence_of_element_located((By.ID, "VV_START_d"))).click()
e  = wait.until( EC.presence_of_element_located((By.CLASS_NAME, "form-control.input-sm")))
e.clear()
e.send_keys(WATER_START_TEMP)
e = wait.until( EC.presence_of_element_located((By.CLASS_NAME, "glyphicon.glyphicon-ok")))
print('C')
e.click()
driver.close()
