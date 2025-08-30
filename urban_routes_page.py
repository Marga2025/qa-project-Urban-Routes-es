import code
import self
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from data import card_number
from urban_routes_utils import retrieve_phone_code
import time

import locators


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.driver_modal = locators.DRIVER_MODAL
        self.request_taxi_button = locators.REQUEST_TAXI_BUTTON
        self.ice_cream_plus_button = locators.ICE_CREAM_BUTTON
        self.blanket_tissues_checkbox = locators.BLANKET_TISSUES_CHECKBOX
        self.message_input = locators.MESSAGE_INPUT
        self.add_card_button = locators.ADD_CARD_BUTTON
        self.telephone_number = locators.TELEPHONE_NUMBER_FIELD
        self.telephone_button = locators.TELEPHONE_BUTTON
        self.mode_comfort_button = locators.MODE_COMFORT_BUTTON
        self.to_field = locators.TO_FIELD
        self.from_field = locators.FROM_FIELD
        # Localizadores que faltaban:
        self.cvv_input = locators.CVV_INPUT
        self.card_input = locators.CARD_INPUT
        self.sms_code_field = locators.SMS_CODE_FIELD
        self.sms_confirm_button = locators.SMS_CONFIRM_BUTTON
        self.next_button = locators.NEXT_BUTTON
        self.card_option = locators.CARD_OPTION
        self.card_add_button = locators.CARD_ADD_BUTTON
        self.payment_close_button = locators.PAYMENT_CLOSE_BUTTON
        self.payment_picker = locators.PAYMENT_PICKER
        self.request_taxi_button = locators.REQUEST_TAXI_BUTTON
        self.driver_info = locators.DRIVER_INFO

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

    def fill_route(self, from_address, to_address):
            """Llenar origen y destino"""
            self.set_from(from_address)
            self.set_to(to_address)

    def check_request_taxi_button(self):
            # Espera hasta que el botón esté presente y clickeable
            button = self.wait.until(EC.element_to_be_clickable(self.request_taxi_button))
            button.click()
            return button.is_enabled()

    def click_mode_comfort_button(self):
        comfort_button = self.wait.until(
            EC.element_to_be_clickable(self.mode_comfort_button))
        comfort_button.click()

        # Verificar múltiples estados
        is_enabled = comfort_button.is_enabled()
        button_classes = comfort_button.get_attribute("class")

        print(f"Botón habilitado: {is_enabled}")
        print(f"Clases del botón: {button_classes}")

        return is_enabled

    def click_telephone_number_button(self):
        # Esperar que el botón esté listo y hacer clic
        telephone_number_button = self.wait.until(EC.element_to_be_clickable(self.telephone_button))
        telephone_number_button.click()

        # Esperar que aparezca el campo de número de teléfono para confirmar que se abrió
        self.wait.until(EC.visibility_of_element_located(self.telephone_number))
        return True

    def add_telephone_number(self, phone):
        # Esperar a que el campo esté clickeable
        phone_field = self.wait.until(EC.element_to_be_clickable(self.telephone_number))

        # Enviar el número directamente
        phone_field.send_keys(phone)

        # Hacer clic en el botón "Siguiente"
        next_button = self.wait.until(EC.element_to_be_clickable(self.next_button))
        next_button.click()

        # Obtener el código de confirmación (¡IMPORTANTE: pasar self.driver!)
        code = retrieve_phone_code(self.driver)

        # Ingresar el código SMS
        code_field = self.wait.until(EC.element_to_be_clickable(self.sms_code_field))
        code_field.send_keys(code)

        # Confirmar el código
        confirm_button = self.wait.until(EC.element_to_be_clickable(self.sms_confirm_button))
        confirm_button.click()

    def open_payment_method_modal(self):
        """Abrir el modal de método de pago"""
        add_payment_btn = self.wait.until(EC.element_to_be_clickable(self.add_card_button))
        add_payment_btn.click()
        print("✅ Modal de método de pago abierto")

    def select_card_payment(self):
        """Selecciona 'Agregar tarjeta' como método de pago"""
        card_option = self.wait.until(EC.element_to_be_clickable(self.card_option))

        # Esperar que deje de estar 'disabled'
        self.wait.until(lambda d: "disabled" not in card_option.get_attribute("class"))

        self.driver.execute_script("arguments[0].scrollIntoView(true);", card_option)
        card_option.click()
        print("✅ Se seleccionó 'Agregar tarjeta'")

    def add_credit_card(self, card_number, cvv_code):
        """Agrega una tarjeta de crédito"""
        try:
            # Número de tarjeta
            card_field = self.wait.until(EC.visibility_of_element_located(self.card_input))
            card_field.clear()
            card_field.send_keys(card_number)

            # CVV
            cvv_field = self.wait.until(EC.visibility_of_element_located(self.cvv_input))
            cvv_field.clear()
            cvv_field.send_keys(cvv_code)

            # Forzar pérdida de foco para habilitar botón
            cvv_field.send_keys(Keys.TAB)
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.click()

            # Esperar botón activo
            add_btn = self.wait.until(EC.element_to_be_clickable(self.card_add_button))
            print("Botón habilitado:", add_btn.is_enabled())
            add_btn.click()
            print("✅ Se hizo clic en 'Agregar tarjeta'")

            # Código SMS
            sms_field = self.wait.until(EC.visibility_of_element_located(self.sms_code_field))
            sms_code = retrieve_phone_code()
            sms_field.send_keys(sms_code)

            confirm_btn = self.wait.until(EC.element_to_be_clickable(self.sms_confirm_button))
            confirm_btn.click()
            print("✅ Código SMS confirmado")

            # Esperar cierre modal SMS
            self.wait.until(EC.invisibility_of_element_located(self.sms_code_field))
            print("✅ Modal de tarjeta cerrado")
        except Exception as e:
            print(f"❌ Error al agregar tarjeta: {e}")

    def close_payment_method_modal(self):
        """Cierra el modal de método de pago"""
        try:
            # Esperar a que aparezca la tarjeta seleccionada (ya agregada)
            self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'pp-value') and contains(., 'Tarjeta')]")
            ))

            # Ahora buscar el botón de cerrar dentro del modal abierto
            close_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.payment-picker.open button.close-button.section-close"))
            )

            # Ejecutar el clic con JS para evitar problemas de superposición
            self.driver.execute_script("arguments[0].click();", close_btn)

            # Esperar que el modal desaparezca
            self.wait.until(EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, "div.payment-picker.open")
            ))
            print("✅ Modal de método de pago cerrado")

        except Exception as e:
            print(f"❌ No se pudo cerrar el modal de método de pago: {e}")

    def enter_message(self, message):
        self.driver.find_element(*self.message_input).send_keys(message)

    def request_blanket_and_tissues(self):
        """Selecciona manta y pañuelos"""
        try:
            checkbox = self.wait.until(EC.presence_of_element_located(self.blanket_tissues_checkbox))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)

            if not checkbox.is_selected():
                self.driver.execute_script("arguments[0].click();", checkbox)

            print("✅ Se seleccionó manta y pañuelos")
        except Exception as e:
            print(f"❌ No se pudo seleccionar manta y pañuelos: {e}")

    def request_ice_cream(self, quantity=2):
        for _ in range(quantity):
            self.driver.find_element(*self.ice_cream_plus_button).click()

    def click_request_taxi(self):
        """Hace clic en el botón 'Pedir un taxi' aunque no esté visible"""
        try:
            button = self.driver.find_element(*self.request_taxi_button)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            self.driver.execute_script("arguments[0].click();", button)
            print("✅ Se hizo clic en 'Pedir un taxi' (forzado con JS)")
            return True
        except Exception as e:
            print(f"❌ No se pudo hacer clic en 'Pedir un taxi': {type(e).__name__}: {str(e)}")
            return False

    def wait_for_driver_info(self):
        """Espera hasta que desaparezca 'Buscando conductor' y aparezca la info del conductor"""
        try:
            # Espera a que se vaya el estado de búsqueda
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "order-spinner")))

            # Ahora espera la info del conductor
            driver_info = WebDriverWait(self.driver, 60).until(
                EC.visibility_of_element_located(self.driver_info)
            )
            print("✅ Apareció la información del conductor")
            return driver_info
        except Exception as e:
            print(f"❌ No se encontró la información del conductor: {type(e).__name__}: {str(e)}")
            return None