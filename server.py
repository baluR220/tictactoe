import socket

players = []

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 9090))

stop_server = False
print('Server is on')
while not stop_server:
    try:
        data, addr = sock.recvfrom(1024)
        if addr not in players:
            players.append(addr)
        print(addr, 'is connected')

        for player in players:
            if addr!= player:
                sock.sendto(data, player)

    except:
        print('Server is off')
        stop_server = True
sock.close()            
