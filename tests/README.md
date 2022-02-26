This directory contains all of the tests using Selenium
- pip3 install selenium webdriver_manager

import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
 
web = webdriver.Chrome(ChromeDriverManager().install())
web.maximize_window()
web.get("https://demoqa.com/automation-practice-form")
 
 
def form():
   time.sleep(3)
   web.find_element_by_id("firstName").send_keys("ABC")
   web.find_element_by_id("lastName").send_keys("XYZ")
   web.find_element_by_id("userEmail").send_keys("ABC@XYZ.com")
   web.find_element_by_xpath("//label[contains(text(),'Male')]").click()
   web.find_element_by_xpath("//input[@id='userNumber']").send_keys(1234567890)
   web.find_element_by_xpath("//label[contains(text(),'Reading')]").click()
   web.find_element_by_xpath("//textarea[@id='currentAddress']").send_keys("Browser Console")
   time.sleep(1)
   web.find_element_by_xpath(
       "//body/div[@id='app']/div[1]/div[1]/div[2]/div[2]/div[1]/form[1]/div[11]/div[1]/button[1]").click()
 
form()