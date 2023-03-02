from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

driver = webdriver.Firefox()
driver.get("https://linkedin.com/uas/login")

time.sleep(4)

username = driver.find_element(By.XPATH,"//input[@name='session_key']") 
password = driver.find_element(By.XPATH,"//input[@name='session_password']") 

username.send_keys("riccardocapellimi91@gmail.com")
password.send_keys("Z6GxtcquCK33zcY")

time.sleep(4)

password = driver.find_element(By.XPATH,"//button[@type='submit']").click()
time.sleep(4)
