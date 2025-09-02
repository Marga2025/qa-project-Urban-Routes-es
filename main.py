
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


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

        self.page.click_telephone_number_button()  # Hace clic en el botón para ingresar el número
        self.page.add_telephone_number(data.phone_number)  # Ingresa el número

        # Encuentra el div donde se muestra el número ingresado
        phone_input = self.driver.find_element(By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[1]")
        number_phone = phone_input.text

        # Verifica que el número ingresado esté en el texto visible del DOM
        assert data.phone_number in number_phone

    def test_add_credit_card(self):
        """Prueba 4: Agregar una tarjeta de crédito"""
        self.page.open_payment_method_modal()
        self.page.select_card_payment()
        self.page.add_credit_card(data.card_number, data.card_code)
        self.page.close_payment_method_modal()

        # Verificación: que el CVV quedó escrito
        cvv_field = self.driver.find_element(By.CSS_SELECTOR, "input#code.card-input")
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
        assert self.page.click_request_taxi()

    def test_wait_for_driver_info(self):
        """Prueba 9: Verificar que aparece la información del conductor"""
        driver_info = self.page.wait_for_driver_info()

        # Verifica que se haya cargado algún texto con la info
        assert driver_info is not None and driver_info.strip() != "", "No apareció la información del conductor"
        print(f"✅ Información del conductor encontrada: {driver_info}")