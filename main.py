import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from urban_routes_utils import retrieve_phone_code


import data
from urban_routes_page import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        chrome_options = Options()
        # chrome_options.add_argument('--headless=new')  # ← COMENTA ESTA LÍNEA
        chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        # Usar webdriver-manager para obtener el ChromeDriver compatible
        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        cls.page = UrbanRoutesPage(cls.driver)
        cls.page.load(data.urban_routes_url)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_set_route(self):
        """Prueba 1: Configurar la dirección"""
        self.page.set_from(data.address_from)
        self.page.set_to(data.address_to)
        assert self.page.get_from() == data.address_from
        assert self.page.get_to() == data.address_to
        assert self.page.check_request_taxi_button()

    def test_select_comfort_tariff(self):
        """Prueba 2: Seleccionar la tarifa Comfort"""
        self.page.click_mode_comfort_button()
        active_tariff = self.driver.find_element(By.XPATH, "//div[contains(@class, 'tcard') and .//div[text()='Comfort']]")
        assert "active" in active_tariff.get_attribute("class")

    def test_fill_phone_number(self):
        """Prueba 3: Rellenar el número de teléfono"""
        self.page.click_telephone_number_button()
        self.page.add_telephone_number(data.phone_number)
        phone_input = self.driver.find_element(By.CLASS_NAME, "np-text")
        assert data.phone_number in phone_input.get_attribute("textContent") or data.phone_number in phone_input.text

    def test_add_credit_card(self):
        """Prueba 4: Agregar una tarjeta de crédito"""
        self.page.add_credit_card(data.card_number, data.card_code)
        cvv_field = self.driver.find_element(By.ID, "code")
        assert cvv_field.get_attribute("value") == data.card_code

    def test_write_message_for_driver(self):
        """Prueba 5: Escribir un mensaje para el controlador"""
        self.page.enter_message(data.message_for_driver)
        message_input = self.driver.find_element(By.ID, "comment")
        assert data.message_for_driver in message_input.get_attribute("value")

    def test_request_blanket_and_tissues(self):
        """Prueba 6: Pedir una manta y pañuelos"""
        self.page.request_blanket_and_tissues()
        checkbox = self.driver.find_element(By.CLASS_NAME, "switch-input")
        assert checkbox.is_selected()

    def test_request_ice_cream(self):
        """Prueba 7: Pedir 2 helados"""
        self.page.request_ice_cream(quantity=2)
        # Verificar que el contador muestra 2
        counter_value = self.driver.find_element(By.CLASS_NAME, "counter-value")
        assert counter_value.text == "2"

    def test_search_taxi(self):
        """Prueba 8: Hacer clic en el botón para buscar un taxi"""
        self.page.click_request_taxi()
        # Esperar a que aparezca el modal de búsqueda de conductor
        wait = WebDriverWait(self.driver, 40)
        search_modal = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "order-header-title")))
        assert search_modal.is_displayed()

    def test_wait_for_driver_info(self):
        """Prueba 9: Verificar que aparece la información del conductor"""
        # Esperar a que aparezca la información del conductor
        wait = WebDriverWait(self.driver, 40)
        driver_info = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "driver-info")))
        assert driver_info.is_displayed()