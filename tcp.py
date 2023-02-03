
''' TCP (socket module) API! 
Accepts both IPv4 and IPv6 addresses
Never use 0x7F in messages'''

__all__ = ['client', 'server', 'DONE', 'STOP']

DONE = 'STOP THE CONNECTION PLEASE PLEASE PLEASE'
STOP = 'MAKE THE SCREEN STOP HANGING PLEASE PLEASE PLEASE'

def client(ip, port, func, start=None, encoding='utf-8'):
    '''TCP client, will use ip and port, things sent will be passed as strings to func, which will
    parse them and return response strings, start is the start string that the client will send
    at first, if func returns tcp.DONE, the connection will terminate'''
    ip = str(ip)
    port = int(port)
    if '.' in ip:
        ipv6 = False
    elif ':' in ip:
        ipv6 = True
    else:
        raise ValueError('Invalid IP')
    if port < 0 or port > 65535:
        raise ValueError('Invalid Port')
    with socket.Socket(socket.AF_INET6 if ipv6 else socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        if start != None:
            if start == DONE:
                raise ValueError('Cannot terminate connection immediately')
            s.sendall(str(start).encode(encoding))
        while True:
            while True:
                data = s.recv(1024)
                if not data:
                    break
            data = data.decode(encoding)
            if data == '':
                break
            new = func(data.d)
            if new == DONE:
                break
            s.sendall((new + chr(0x7F).encode(encoding))

def server(port, func, start=None, ipv6=True, encoding='utf-8'):
    '''TCP server, will block forever unless func returns tcp.STOP, func is function that takes in 
    strings as input from the client and outputs responses, start is string to be sent at first, if 
    func returns tcp.DONE, connection will terminate'''
    port = int(port)
    if port < 0 or port > 65535:
        raise ValueError('Invalid Port')
    with socket.Socket(socket.AF_INET6 if ipv6 else socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('::1' if ipv6 else '127.0.0.1', port))
        while True:
            if start != None:
                if start == STOP:
                    raise ValueError('Cannot stop on first connection')
            while True:
                while True:
                    nbyte = 'x'
                    data = b''
                    stop = False
                    while nbyte != chr(0x7F):
                        nbyte = s.recv(1)
                        if nbyte == b'':
                            stop = True
                            break
                        data += nbyte
                    if stop:
                        break
                    data = data.decode(encoding)
                    if data == '':
                        break
                    new = func(data.d)
                    if new == DONE:
                        break
                    if new == STOP:
                        return
                    s.sendall(new.encode(encoding))
