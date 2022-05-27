import socket
import os
from ast import literal_eval
import sys
filename = sys.argv[1]
f = open(filename, 'r')
lines = f.readlines()
ls = []
for line in lines:
    ls.append(line)

ls = list(set(ls)) 
lines = ls

count = 1

for line in lines:
    fs = open("cached.txt", 'r')
    found = 0
    cnt = 0
    cacheLines = fs.readlines()
    cl = []
    for cacheLine in cacheLines:
        cl.append(cacheLine.split(' ')[0]+' '+cacheLine.split(' ')[1]+' '+cacheLine.split(' ')[2]+' '+cacheLine.split(' ')[3]+'\n')

    for l in cl:
        if l == line:
            found = 1
            break
        cnt = cnt + 1
    if found == 1:
        print(cacheLines[cnt])
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        string = line
        method = string.split(' ')[0]
        fileName = string.split(' ')[1]
        hostName = string.split(' ')[2]
        portNumber = 80
        portNumber = string.split(' ')[3]
        if method == 'POST':
            fb = open("contents.txt", 'r')
            blines = fb.readlines()
            body = []
            for lineBody in blines:
                body.append(lineBody)
            request = method+" "+fileName+" "+"HTTP/1.0\r\n"+"Host: "+hostName+":"+portNumber+"\r\n\r\n" + str(body)+"\r\n"
        else:
            request = method+" "+fileName+" "+"HTTP/1.0\r\n"+"Host: "+hostName+":"+portNumber+"\r\n\r\n"
        
        packet = bytes(request, 'utf-8')
    
        s.connect((socket.gethostbyname(hostName), int(portNumber)))
        print('Connected to server successfully')
        print('Request:')
        print(request)
        s.send(packet)
        print('Request sent sucessfully\n')
    
        if method == 'GET':
            split_tup = os.path.splitext(fileName)
            file_extension = split_tup[1]
            if file_extension == '.txt':
                response = s.recv(2048)
                if response.decode('utf-8').split('\r\n\r\n')[1] == "Error 404 Not Found\r\n":
                    print("No response from server")
                    fc = open("cached.txt", 'a')
                    st = string + response.decode('utf-8')
                    st = st.replace("\r\n\r\n", " ")
                    st = st.replace("\n", " ")
                    st = st.replace("\r", " ")+"\n"
                    fc.write(st)
                    s.close()
                else:
                    data = response.decode('utf-8').split('\r\n\r\n')[1]
                    fc = open("cached.txt", 'a')
                    st = string + response.decode('utf-8')
                    st = st.replace("\r\n\r\n", " ")
                    st = st.replace("\n", " ")
                    st = st.replace("\r", " ")+"\n"
                    fc.write(st)
                    fr = open("file"+str(count)+".txt", 'w')
                    dataArr = literal_eval(data)
                    for x in dataArr:
                        fr.write(x)
            elif file_extension == '.png':
                s.close()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((socket.gethostbyname(hostName), 12346))
                packet = bytes(fileName, 'utf-8')
                sock.send(packet)
                f = open("file"+str(count)+".png", "wb")
                data = None
                while True:
                    m = sock.recv(1024)
                    data = m
                    if m:
                        while m:
                            m = sock.recv(1024)
                            data += m
                        else:
                            break
                f.write(data)
                f.close()
            else:
                response = s.recv(2048)
                if response.decode('utf-8').split('\r\n\r\n')[1] == "Error 404 Not Found\r\n":
                    print("No response from server")
                    fc = open("cached.txt", 'a')
                    st = string + response.decode('utf-8')
                    st = st.replace("\r\n\r\n", " ")
                    st = st.replace("\n", " ")
                    st = st.replace("\r", " ")+"\n"
                    fc.write(st)
                    s.close()
                else:
                    data = response.decode('utf-8').split('\r\n\r\n')[1]
                    fc = open("cached.txt", 'a')
                    st = string + response.decode('utf-8')
                    st = st.replace("\r\n\r\n", " ")
                    st = st.replace("\n", " ")
                    st = st.replace("\r", " ")+"\n"
                    fc.write(st)
                    fr = open("file"+str(count)+".html", 'w')
                    dataArr = literal_eval(data)
                    for x in dataArr:
                        fr.write(x)
            count = count + 1
        else:
            response = s.recv(2048)
            fc = open("cached.txt", 'a')
            st = string + response.decode('utf-8')
            st = st.replace("\r\n\r\n", " ")
            st = st.replace("\r\n", " ")
            st = st.replace("\n", " ")+'\n'
            fc.write(st)     
        s.close()