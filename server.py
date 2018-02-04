import socket
import logging
import struct
import select
import threading
import re

def send_all(sock,data):
    send_bytes = 0
    while True:
        n = sock.send(data[send_bytes:])
        if n < 0:
            return n
        send_bytes += n
        if send_bytes == len(data):
            return send_bytes


def handle_connect(client,client_addr):
    request = client.recv(1024)
    content = b'HTTP/1.x 200 ok\r\nContent-Type: text/html\r\n\r\n'
    
    print("request is \n",request)
    query=request.split()[1]
    print(query)
    m = re.search(b'/?',query)
    if m:
        name = query.split(b'=')[1].split(b'&')[0]
        password = query.split(b'=')[2].split(b'&')[0]
        kind = query.split(b'=')[3]
        print("name = ",name," password = ",password,"kind = ",kind)
        if(kind == b'0'):
            content += b'register'
            #re=register(name,password)
        if(kind == b'1'):
            content += b'sign in'
            #re=register(name,password)

    else:
        print('error')

    send_all(client,content)



def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('',5555))
    server.listen(15)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        while True:
            c, addr = server.accept()
            print(addr)
            t = threading.Thread(target = handle_connect,args =(c,addr))
            t.start()
    except socket.error as e:
        logging.error(e)
    except KeyboardInterrupt:
        server.close()

if __name__=="__main__":
    main()