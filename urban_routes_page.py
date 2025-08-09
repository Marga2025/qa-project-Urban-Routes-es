from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        self.driver.get(url)

    def set_address(self, field_id, address):
        field = self.wait.until(EC.visibility_of_element_located((By.ID, field_id)))
        field.clear()
        field.send_keys(address)
        suggestion = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "suggest__item")))
        suggestion.click()

    def select_comfort_tariff(self):
        tariff = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "tariff__card")))
        tariff.click()

    def enter_phone_number(self, number):
        phone_input = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "input__control")))
        phone_input.clear()
        phone_input.send_keys(number)

    def submit_phone_number(self):
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "button")))
        button.click()

    def enter_confirmation_code(self, code):
        code_input = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "verification__code-input")))
        code_input.send_keys(code)

    def enter_card_details(self, number, code):
        card_field = self.wait.until(EC.presence_of_element_located((By.NAME, "number")))
        card_field.send_keys(number)
        code_field = self.driver.find_element(By.NAME, "code")
        code_field.send_keys(code)

    def write_message_to_driver(self, message):
        text_area = self.driver.find_element(By.NAME, "comment")
        text_area.send_keys(message)

    def request_blanket_and_tissues(self):
        for item in ["towels", "napkins"]:
            checkbox = self.driver.find_element(By.NAME, item)
            checkbox.click()

    def order_ice_cream(self, quantity):
        plus_button = self.driver.find_element(By.CLASS_NAME, "counter__button_plus")
        for _ in range(quantity):
            plus_button.click()

    def submit_order(self):
        order_button = self.driver.find_element(By.CLASS_NAME, "order-button__button")
        order_button.click()

    def is_searching_modal_visible(self):
        modal = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "searching-screen__title")))
        return modal.is_displayed()