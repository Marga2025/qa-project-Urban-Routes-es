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
        """Hace clic en el botón para ingresar el número de teléfono"""
        try:
            button = self.wait.until(
                EC.element_to_be_clickable(self.telephone_button)
            )
            button.click()
            print("✅ Se hizo clic en el botón para ingresar número de teléfono")
        except Exception as e:
            print(f"❌ Error al hacer clic en el botón de teléfono: {e}")

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
        modal_btn = self.wait.until(EC.element_to_be_clickable(self.add_card_button))
        modal_btn.click()
        print("✅ Modal de métodos de pago abierto")

    # --- Cerrar modal ---
    def close_payment_method_modal(self):
        close_btn = self.wait.until(EC.element_to_be_clickable(self.payment_close_button))
        close_btn.click()
        print("✅ Modal de métodos de pago cerrado")

    # --- Seleccionar opción de agregar tarjeta ---
    def select_card_payment(self):
        option = self.wait.until(EC.element_to_be_clickable(self.card_option))
        option.click()
        print("✅ Opción 'Agregar tarjeta' seleccionada")

    # --- Llenar número de tarjeta ---
    def set_card_number_field(self, card_number):
        card_input = self.wait.until(EC.presence_of_element_located(self.card_input))
        self.driver.execute_script("arguments[0].value = arguments[1];", card_input, card_number)
        print(f"👉 Número de tarjeta ingresado: {card_number}")

    # --- Llenar CVV y simular TAB ---
    def set_card_code_field(self, card_code):
        cvv_input = self.wait.until(EC.presence_of_element_located(self.cvv_input))
        self.driver.execute_script("arguments[0].value = arguments[1];", cvv_input, card_code)

        # Simular pérdida de foco (TAB)
        ActionChains(self.driver).send_keys(Keys.TAB).perform()
        time.sleep(0.5)

        cvv_value = self.driver.execute_script("return arguments[0].value;", cvv_input)
        print(f"👉 CVV ingresado: {cvv_value}")

    # --- Clic en botón Agregar ---
    def click_add_button(self):
        add_btn = self.wait.until(EC.element_to_be_clickable(self.card_add_button))
        self.driver.execute_script("arguments[0].click();", add_btn)
        print("✅ Botón 'Agregar' presionado")

    # --- Flujo completo ---
    def add_credit_card(self, card_number, card_code):
        """Ingresa número de tarjeta y CVV"""
        try:
            # Campo número tarjeta
            card_field = self.wait.until(EC.presence_of_element_located(self.card_input))
            card_field.clear()
            card_field.send_keys(card_number)
            print(f"👉 Número de tarjeta ingresado: {card_number}")

            # Campo CVV
            cvv_field = self.wait.until(EC.presence_of_element_located(self.cvv_input))
            cvv_field.clear()
            cvv_field.send_keys(card_code)
            print(f"👉 CVV ingresado: {card_code}")

            # 🔑 Forzar pérdida de foco: presionamos TAB
            cvv_field.send_keys(Keys.TAB)

            # Ahora sí: esperar botón "Agregar"
            add_btn = self.wait.until(EC.element_to_be_clickable(self.card_add_button))
            add_btn.click()
            print("✅ Botón 'Agregar' presionado")

        except Exception as e:
            print(f"❌ Error al agregar tarjeta: {e}")
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
        """Hace clic en el botón 'Pedir un taxi' y verifica que aparezca el modal"""
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.request_taxi_button)
            )
            button.click()
            print("✅ Se hizo clic en 'Pedir un taxi'")
            time.sleep(2)  # Agregar esta línea para dar tiempo al modal
            return True
        except:
            button = self.driver.find_element(*self.request_taxi_button)
            self.driver.execute_script("arguments[0].click();", button)
            print("✅ Se hizo clic en 'Pedir un taxi' (con JS)")
            time.sleep(2)  # Agregar esta línea también
            return True

    def wait_for_driver_info(self, timeout=45):
        """Espera a que aparezca la info del conductor en .drive-preview y devuelve su texto."""
        try:
            # 1) Esperar a que exista el contenedor .drive-preview en el DOM
            container = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.driver_info)  # self.driver_info = (By.CLASS_NAME, "drive-preview")
            )

            # 2) Traerlo al viewport y esperar visibilidad
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", container)
            WebDriverWait(self.driver, 10).until(EC.visibility_of(container))

            # 3) Esperar a que tenga contenido (texto no vacío)
            end = time.time() + 30  # tiempo adicional para que cargue el texto interno
            text = container.text.strip()
            while text == "" and time.time() < end:
                time.sleep(0.5)
                text = container.text.strip()

            if text:
                print(f"✅ Información del conductor encontrada: {text}")
                return text

            print("❌ El contenedor '.drive-preview' apareció pero sin texto.")
            return None

        except Exception as e:
            print(f"❌ No apareció la información del conductor: {type(e).__name__}: {e}")
            return None