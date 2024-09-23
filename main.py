import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_driver():
    # Определяем путь к chromedriver.exe
    chromedriver_path = r"C:\path\to\chromedriver.exe"

    # Создаем сервис с путем к chromedriver
    service = Service(chromedriver_path)

    # Создаем драйвер Chrome
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver


@pytest.fixture(scope="module")
def driver():
    yield setup_driver()


def test_purchase(driver):
    # Авторизация
    driver.get("https://saucedemo.com/")
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )
    username_input.send_keys("standard_user")
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("secret_sauce")
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

    # Выбор товара
    product_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name"))
    )
    product_name.click()

    # Добавление в корзину
    cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn_inventory"))
    )
    cart_button.click()

    # Переход в корзину
    cart_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Cart')]"))
    )
    cart_link.click()

    # Оформление покупки
    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='checkout']"))
    )
    checkout_button.click()

    # Заполнение формы покупки
    first_name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "first-name"))
    )
    first_name_input.send_keys("John")
    last_name_input = driver.find_element(By.ID, "last-name")
    last_name_input.send_keys("Doe")
    postal_code_input = driver.find_element(By.ID, "postal-code")
    postal_code_input.send_keys("12345")

    # Завершение покупки
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='continue']"))
    )
    continue_button.click()

    # Подтверждение покупки
    finish_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='finish']"))
    )
    finish_button.click()

    # Проверка успешного завершения покупки
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
    ).text
    assert "Thank you for your order" in success_message, "Purchase not successful"

    print("Тест пройден успешно")


# Запуск теста
if __name__ == "__main__":
    pytest.main([__file__, "-v"])

