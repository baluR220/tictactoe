import socket

server = input('Connect to: ')
x = 15
y = 20
count = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((server, 9090))

data_send = str(x) + '_' + str(y) + str(count)
sock.sendto(data_send.encode(), (server, 9090))
sock.setblocking(0)
data_recv = sock.recv(1024)
print(data_recv)
