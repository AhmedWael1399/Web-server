import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 12346))

while True:
    s.listen()
    c, addr = s.accept()
    print('{} connected.'.format(addr))
    filename = c.recv(1024).decode('utf-8')
    f = open(filename, "rb")
    l = os.path.getsize(filename)
    m = f.read(l)
    c.sendall(m)
    f.close()
    print("Done sending...")
    c.close()