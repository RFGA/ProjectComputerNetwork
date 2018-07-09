import socket
import os
from save_file import savefile
f = open('index.html', 'r')
homepage = f.read()
##g = open('Links/ecomp.jpg', 'r')
##figure = g.read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(s)

s.bind(('', 8081))
s.listen(5)
#conn, addr = s.accept()

while True:
    conn, addr = s.accept()

    data = str(conn.recv(500000))
    print(data)
    dataParse = data.split(' ')
    page = ('HTTP/1.0 200 OK\r\n' +
                 'Content-Type: text/html\r\n' +
                 'Content-Length: ' + str(len(homepage)) + '\r\n\r\n' + homepage)
    msg = ('HTTP/1.0 201 Created\r\n'+
           'Location: http://localhost:8081/data/1\r\n\r\n')
    if 'GET' in str(data):
        dataParse = data.split(' ')
        conn.sendall(page.encode())
    elif 'POST' in str(data):
        print("ENTROU NO PST")
       ## conn.sendall(msg.encode())
        conn.sendall(msg.encode())
        data = str(conn.recv(500000))
        print(data)
    else:
        print('queisdf')
        if not os.path.exists(os.path.join(os.getcwd(), 'tmp')):
            # Senão nós o criamos
            os.mkdir(os.path.join(os.getcwd(), 'tmp'))

    conn.close()
s.close()

