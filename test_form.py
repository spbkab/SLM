import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")  # run without UI
    options.add_argument("--no-sandbox")  # required in many CI environments
    options.add_argument("--disable-dev-shm-usage")  # overcome limited /dev/shm size on Linux

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_successful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")

    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    wait = WebDriverWait(driver, 10)
    secure_area_header = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h2")))

    assert "Secure Area" in secure_area_header.text
    assert "Welcome to the Secure Area" in driver.page_source

def test_unsuccessful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")

    driver.find_element(By.ID, "username").send_keys("invalid_user")
    driver.find_element(By.ID, "password").send_keys("invalid_password")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    flash_element = driver.find_element(By.CLASS_NAME, "flash")
    assert "Your username is invalid!" in flash_element.text