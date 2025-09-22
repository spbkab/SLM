import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

# Fixture для инициализации драйвера браузера
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

# Тест на успешный логин
@pytest.mark.smoke
@allure.title("Successful login test")
@allure.description("Verify successful authentication using valid credentials.")
def test_successful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")

    # Заполняем поля формы
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")

    # Кликаем по кнопке входа
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Ждём загрузки области Secure Area
    wait = WebDriverWait(driver, 10)
    secure_area_header = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h2")))

    # Проверяем наличие ожидаемого текста
    assert "Secure Area" in secure_area_header.text
    assert "Welcome to the Secure Area" in driver.page_source

# Тест на неуспешный логин
@pytest.mark.regression
@allure.title("Unsuccessful login test")
@allure.description("Verify that incorrect credentials lead to an error message.")
def test_unsuccessful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")

    # Заполняем форму неправильными данными
    driver.find_element(By.ID, "username").send_keys("invalid_user")
    driver.find_element(By.ID, "password").send_keys("invalid_password")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Проверяем появление уведомления об ошибке
    flash_element = driver.find_element(By.CLASS_NAME, "flash")
    assert "Your username is invalid!" in flash_element.text