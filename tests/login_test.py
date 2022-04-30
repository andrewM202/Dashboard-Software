# from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

@pytest.mark.auth
def test_login():
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    # driver.maximize_window()
    driver.get("http://127.0.0.1:8000/")
    # Click on demo pages
    driver.find_element(by=By.XPATH, value=('//*[@id="example-navbar-warning"]/ul[2]/li[1]/div/a')).click()
    # Click on login
    driver.find_element(by=By.XPATH, value=('//*[@id="example-navbar-warning"]/ul[2]/li[1]/div/div/a[1]')).click()
    # Enter username into the username input
    driver.find_element(by=By.XPATH, value=('//*[@id="grid-email"]')).send_keys("admin")
    # Enter password into the password input
    driver.find_element(by=By.XPATH, value=('//*[@id="grid-password"]')).send_keys("password")
    # Click submit button
    driver.find_element(by=By.XPATH, value=('//*[@id="SignUpForm"]/div[4]/button')).click()
    # If we see the h6 dashboards text then we know we are logged in
    try:
        # Wait up till 5 seconds to see if the element exists
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="SideBarNav"]/div/div/h6[1]'))
        WebDriverWait(driver, 5).until(element_present)
    except Exception:
        print ("Timed out waiting for page to load")
        driver.quit()
        assert False
    driver.quit()
    assert True

if __name__ == '__main__':
    test_login()