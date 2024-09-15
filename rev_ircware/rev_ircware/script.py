from pwn import *

server = listen(8000)

conn = server.wait_for_connection()

print(conn.recvline().decode().strip())
print(conn.recvline().decode().strip())
print(conn.recvline().decode().strip())

conn.send(b"PRIVMSG #secret :@pass A")

if "Accepted" in conn.recvline().decode().strip():
    conn.sendline(b"PRIVMSG #secret :@flag")
    print(conn.recvline().decode().strip())


conn.close()
