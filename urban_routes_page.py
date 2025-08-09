from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import locators


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
        # Esperar a que el elemento esté presente
        from_element = self.wait.until(EC.presence_of_element_located(self.from_field))

        # Usar JavaScript para hacer foco y limpiar el campo
        self.driver.execute_script("arguments[0].focus();", from_element)
        self.driver.execute_script("arguments[0].value = '';", from_element)

        # Enviar las teclas
        from_element.send_keys(from_address)

    def set_to(self, to_address):
        # Esperar a que el elemento esté presente
        to_element = self.wait.until(EC.presence_of_element_located(self.to_field))

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
        telephone_number_button = self.wait.until(EC.element_to_be_clickable(self.telephone_button))
        telephone_number_button.click()
        return telephone_number_button.is_enabled()

    def add_telephone_number(self, phone):
        self.driver.find_element(*self.telephone_number).send_keys(phone)
        return self.driver.find_element(*self.to_field).get_property('value')

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
