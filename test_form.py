import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


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


    assert "Secure Area" in driver.page_source
    assert "Welcome to the Secure Area" in driver.page_source


def test_unsuccessful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")


    driver.find_element(By.ID, "username").send_keys("invalid_user")
    driver.find_element(By.ID, "password").send_keys("invalid_password")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()


    assert "Your username is invalid!" in driver.page_source
