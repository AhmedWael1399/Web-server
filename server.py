
import socket

from _thread import *
import threading

from ast import literal_eval

import os

def threaded(c):
    if threading.active_count() == 1:
        c.settimeout(15)
    elif threading.active_count() > 1 and threading.active_count() < 5:
        c.settimeout(10)
    elif threading.active_count() >= 5 and threading.active_count() < 10:
        c.settimeout(8)
    elif threading.active_count() >= 10:
        c.settimeout(5)
    while True:
        try:
            request = c.recv(2048).decode('utf-8')
            
            if not request:
                print('No request from client')
                break
        
            method = request.split(' ')[0]
            filename = request.split(' ')[1]
            version = request.split(' ')[2]
            data = request.split('\r\n\r\n')[1]

            if method == 'GET':
                split_tup = os.path.splitext(filename)
                file_extension = split_tup[1]
                if file_extension == ".png":
                    break
                else:
                    try:
                        with open(filename, 'r') as file:
                            blines = file.readlines()
                            body = []
                            for lineBody in blines:
                                body.append(lineBody)
                            response = version + " " + "200 OK\r\n\r\n" + str(body) + "\r\n"
                            c.send(bytes(response, 'utf-8'))
                    except FileNotFoundError:
                        response = version+ " " + "404 Not Found\r\n\r\n" + "Error 404 Not Found" + "\r\n"
                        c.send(bytes(response, 'utf-8'))

            else:
                fp = open(filename, 'w')
                dataArr = literal_eval(data)
                for x in dataArr:
                    fp.write(x)
                response = version + " " + "200 OK\r\n\r\n"
                c.send(bytes(response, 'utf-8'))

                
            request = None 
        except socket.timeout:
            c.close()
            print("Connection timeout")
            break
    c.close()
    print("Client disconnected")


host = "127.0.0.1"

port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
print("socket binded to port", port)
print("socket is listening")

while True:
    s.listen()
    c, addr = s.accept()

    print('Connected to :', addr[0], ':', addr[1])

    start_new_thread(threaded, (c,))