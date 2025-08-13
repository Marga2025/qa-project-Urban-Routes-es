from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import locators
from urban_routes_utils import retrieve_phone_code


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.driver_modal = locators.DRIVER_MODAL
        self.request_taxi_button = locators.REQUEST_TAXI_BUTTON
        self.ice_cream_plus_button = locators.ICE_CREAM_BUTTON
        self.blanket_tissues_checkbox = locators.BLANKET_CHECKBOX
        self.message_input = locators.MESSAGE_INPUT
        self.add_card_button = locators.ADD_CARD_BUTTON
        self.telephone_number = locators.TELEPHONE_NUMBER_FIELD
        self.telephone_button = locators.TELEPHONE_BUTTON
        self.mode_comfort_button = locators.MODE_COMFORT_BUTTON
        self.to_field = locators.TO_FIELD
        self.from_field = locators.FROM_FIELD

    def load(self, url):
        self.driver.get(url)

    def set_from(self, from_address):
        from_element = self.wait.until(EC.presence_of_element_located(self.from_field))
        self.driver.execute_script("arguments[0].focus();", from_element)
        self.driver.execute_script("arguments[0].value = '';", from_element)
        from_element.send_keys(from_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_attribute("value")

    def set_to(self, to_address):
        to_element = self.wait.until(EC.presence_of_element_located(self.to_field))
        self.driver.execute_script("arguments[0].focus();", to_element)
        self.driver.execute_script("arguments[0].value = '';", to_element)
        to_element.send_keys(to_address)

    def get_to(self):
        to_element = self.wait.until(EC.presence_of_element_located(self.to_field))
        return to_element.get_attribute("value")

        # Usar JavaScript para hacer foco y limpiar el campo
        self.driver.execute_script("arguments[0].focus();", to_element)
        self.driver.execute_script("arguments[0].value = '';", to_element)

        # Enviar las teclas
        to_element.send_keys(to_address)


    def check_request_taxi_button(self):
        self.driver.find_element(*self.request_taxi_button).click()
        return self.driver.find_element(*self.request_taxi_button).is_enabled()

    def click_mode_comfort_button(self):
        comfort_button = self.wait.until(
            EC.element_to_be_clickable(self.mode_comfort_button))
        comfort_button.click()
        return comfort_button.is_enabled()

    def click_telephone_number_button(self):
        # Esperar que el botón esté listo y hacer clic
        telephone_number_button = self.wait.until(EC.element_to_be_clickable(self.telephone_button))
        telephone_number_button.click()

        # Esperar que aparezca el campo de número de teléfono para confirmar que se abrió
        self.wait.until(EC.visibility_of_element_located(self.telephone_number))
        return True

    def add_telephone_number(self, phone):
        # Esperar campo de teléfono y limpiarlo
        phone_field = self.wait.until(EC.element_to_be_clickable(self.telephone_number))
        phone_field.clear()
        phone_field.send_keys(phone)

        # Botón para confirmar teléfono
        next_button = self.wait.until(EC.element_to_be_clickable(self.telephone_button))
        next_button.click()

        # Esperar campo de SMS antes de obtener código
        sms_field = self.wait.until(EC.element_to_be_clickable(locators.SMS_CODE_FIELD))

        # Obtener código desde los logs de red
        code = retrieve_phone_code(driver=self.driver)
        sms_field.send_keys(code)

        # Confirmar SMS
        confirm_button = self.wait.until(EC.element_to_be_clickable(locators.SMS_CONFIRM_BUTTON))
        confirm_button.click()

    def add_credit_card(self, card_number, code):
        self.driver.find_element(*self.add_card_button).click()
        self.driver.find_element(By.ID, 'number').send_keys(card_number)
        self.driver.find_element(By.ID, 'code').send_keys(code)

    def enter_message(self, message):
        self.driver.find_element(*self.message_input).send_keys(message)

    def request_blanket_and_tissues(self):
        self.driver.find_element(*self.blanket_tissues_checkbox).click()

    def request_ice_cream(self, quantity=2):
        for _ in range(quantity):
            self.driver.find_element(*self.ice_cream_plus_button).click()

    def wait_for_driver_info(self):
        self.wait.until(
            EC.visibility_of_element_located(self.driver_modal)
        )
