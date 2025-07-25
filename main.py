from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def open(self, url):
        self.driver.get(url)
        print(f"Página abierta: {url}")
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#from")))

    def select_comfort_tariff(self):
        comfort_button = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-for='tariff-card-4']")
        ))
        comfort_button.click()

    def enter_from_address(self, address):
        from_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#from")))
        from_input.clear()
        from_input.send_keys(address)

    def submit_order(self):
        order_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='order-button']")))
        order_button.click()


class TestUrbanRoutes:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(3)

    def test_order_taxi(self):
        try:
            page = UrbanRoutesPage(self.driver)
            page.open("https://cnt-66da170e-4d0a-4c9b-801e-4c44998fbff8.containerhub.tripleten-services.com?lng=es")
            page.select_comfort_tariff()
            page.enter_from_address("East 2nd Street, 601")
            time.sleep(2)  # Espera para visualizar el campo completado
            page.submit_order()
            time.sleep(5)
            print("Orden completada exitosamente.")
        except Exception as e:
            print(f"Error durante la ejecución: {e}")
        finally:
            self.driver.quit()


if __name__ == "__main__":
    TestUrbanRoutes().test_order_taxi()