import socket

f = open('index.html', 'r')
homepage = f.read()
##g = open('Links/ecomp.jpg', 'r')
##figure = g.read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(s)

s.bind(('', 8093))
s.listen(5)
#conn, addr = s.accept()

while True:
    conn, addr = s.accept()

    data = str(conn.recv(2000))
    print(data)
    dataParse = data.split(' ')
    print(homepage)
    page = ('HTTP/1.0 200 OK\r\n' +
                 'Content-Type: text/html\r\n' +
                 'Content-Length: ' + str(len(homepage)) + '\r\n\r\n' + homepage)
    conn.sendall(page.encode())
    if dataParse[0] == "GET":
        dataParse = data.split(' ')
        if dataParse[1] == '/':
            conn.sendall('HTTP/1.0 200 OK\r\n' +
                         'Content-Type: text/html\r\n' +
                         'Content-Length: ' + str(len(homepage)) + '\r\n\r\n' +
                          (homepage))
        else:
            conn.sendall('HTTP/1.0 200 OK\r\n' +
                         'Content-Type: image/jpeg\r\n' +
                         'Content-Length: ' + str(len(figure)) + '\r\n\r\n' +
                          (figure))


    conn.close()
s.close()
