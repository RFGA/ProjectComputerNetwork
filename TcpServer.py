import socket
import os
from cryptography.fernet import Fernet

f = open('index.html', 'r')
g = open('message.html', 'r')
homepage = f.read()
message = g.read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(s)

s.bind(('', 8081))
s.listen(5)

def encrypt(txt):
    chave = Fernet.generate_key()
    suite_cifrada = Fernet(chave)
    texto_cifrado = suite_cifrada.encrypt(txt.encode())
    return chave, texto_cifrado

def decrypt(txt,chave):
    suite_cifrada = Fernet(chave)
    texto_decifrado = suite_cifrada.decrypt(txt)
    return texto_decifrado

while True:

    conn, addr = s.accept()

    data = str(conn.recv(5000))
    print(data)


    dataParse = data.split(' ')
    page = ('HTTP/1.0 200 OK\r\n' +
                 'Content-Type: text/html\r\n' +
                 'Content-Length: ' + str(len(homepage)) + '\r\n\r\n' + homepage)


    if 'GET' in str(data):
        dataParse = data.split(' ')
        conn.sendall(page.encode())
    elif 'POST' in str(data):
        if '/encrypt' in str(data):


            print(data)
            text = data
            text = data[data.find('name="filename"')+len('name="filename"________'):]
            text = text[:text.find('\\r\\n')]
            chave, texto = encrypt(text)
            message = message.replace('msg','Chave:'+str(chave)[2:len(str(chave))-1]+'        Mensagem:'+ str(texto)[2:len(str(texto))-1])
            pageMensagem = ('HTTP/1.0 200 OK\r\n' +
                'Content-Type: text/html\r\n' +
                'Content-Length: ' + str(len(message)) + '\r\n\r\n' + message)
            conn.sendall(pageMensagem.encode())
        elif '/decrypt' in str(data):
            text = data
            text = data[data.find('name="filename"') + len('name="filename"________'):]
            text = text[:text.find('\\r\\n')]
            chave = text[text.find('Chave:')+len('Chave:'):text.find('        Mensagem:')]
            msg = text[text.find('        Mensagem:')+len('        Mensagem:'):]
            message = message.replace('msg','Mensagem:  '+decrypt(chave,msg.encode()))
            pageMensagem = ('HTTP/1.0 200 OK\r\n' +
                            'Content-Type: text/html\r\n' +
                            'Content-Length: ' + str(len(message)) + '\r\n\r\n' + message)
            conn.sendall(pageMensagem.encode())
            print(data)


    else:
        if not os.path.exists(os.path.join(os.getcwd(), 'tmp')):
            # Senão nós o criamos
            os.mkdir(os.path.join(os.getcwd(), 'tmp'))

    conn.close()
s.close()

