import requests
import json
import logging
from stem import Signal
from stem.control import Controller
from datetime import datetime, timedelta
import time
import subprocess

# Configuración de logging
logging.basicConfig(level=logging.INFO)

# Configuración del proxy para Tor
proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

# URL de la API en la red Tor
api_url = "http://alphvmmm27o3abo3r2mlmjrpdmzle3rykajqc5xsj7j7ejksbpsa36ad.onion/api/blog/all/0/9"

# Función para realizar una solicitud a la API y devolver el resultado como JSON
def make_tor_request(url):
    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()  # Lanza una excepción para errores HTTP

        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during the request: {str(e)}")
        return None

# Función para notificar y analizar las actualizaciones
def check_and_notify():
    # Realizar la solicitud a la API en Tor
    data = make_tor_request(api_url)

    # Verificar si la solicitud fue exitosa y contiene datos
    if data is not None:
        # Analizar y procesar los datos según sea necesario
        logging.info("Received data from the API:")
        logging.info(json.dumps(data, indent=2))

        # Puedes agregar lógica adicional aquí para notificar o realizar otras acciones con los datos recibidos
        # Por ejemplo, comparar con versiones anteriores, enviar notificaciones, etc.

# Función para cambiar la identidad en Tor (obtener una nueva IP)
def change_tor_identity():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)


def send_terminal_notification(message):
    try:
        subprocess.run(["wall", message])
    except Exception as e:
        logging.error(f"Error sending terminal notification: {str(e)}")

# Función principal del script
def main():
    while True:
        # Verificar y notificar las actualizaciones
        check_and_notify()

        # Cambiar la identidad en Tor cada día (24 horas)
        time.sleep(24 * 60 * 60)
        change_tor_identity()
        # Enviar notificación a la terminal
        send_terminal_notification("El script se ha ejecutado y verificado las actualizaciones.")

if __name__ == "__main__":
    main()