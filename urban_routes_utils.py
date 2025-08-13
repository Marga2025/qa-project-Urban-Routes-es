import json
import time
from selenium.common.exceptions import WebDriverException

def retrieve_phone_code(driver) -> str:
    """
    Intenta recuperar el código de confirmación del teléfono desde los logs
    de rendimiento del navegador. Reintenta hasta 10 veces con 1 segundo
    de espera entre intentos.
    """
    for _ in range(10):
        try:
            # Filtrar logs relacionados con la petición del número
            logs = [
                log["message"]
                for log in driver.get_log('performance')
                if 'api/v1/number?number' in log.get("message", "")
            ]

            # Revisar los logs en orden inverso (más recientes primero)
            for log in reversed(logs):
                message_data = json.loads(log)["message"]

                # Obtener el cuerpo de la respuesta de la red
                body = driver.execute_cdp_cmd(
                    'Network.getResponseBody',
                    {'requestId': message_data["params"]["requestId"]}
                )

                # Extraer solo los dígitos
                code = ''.join([ch for ch in body['body'] if ch.isdigit()])
                if code:
                    return code

        except WebDriverException:
            pass  # Ignorar el error y seguir intentando

        time.sleep(1)  # Espera antes de volver a intentar

    # Si no se encontró el código después de los intentos
    raise Exception("No se encontró el código de confirmación del teléfono.")
