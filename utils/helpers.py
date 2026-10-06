from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(driver):
    driver.get("https://www.saucedemo.com/")

    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    assert "/inventory.html" in driver.current_url, "Error! Login failed: No se redirigió a la página de inventario (/inventory.html)."
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.url_contains("/inventory.html")
    )