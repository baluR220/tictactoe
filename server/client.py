import socket, subprocess, sys 
from tkinter import *

#server = '109.233.239.229'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.sendto(('Hello').encode(), (server, 11719))
print('Connection is on')

master = Tk()
master.title('TTT_online')
main_canvas = Canvas(master, width=400, height=500, bg='white')
main_canvas.pack()

def find_ip_win():
    my_ip = subprocess.check_output(['nslookup', 'myip.opendns.com.', 'resolver1.opendns.com'])
    my_ip = my_ip.decode('cp1251')[-20:-4]
    for i in my_ip:
        if not i.isdigit():
            continue
        else:
            strt = my_ip.find(i)
            break
    my_ip = my_ip[strt:]
    return my_ip

if sys.platform == 'linux':
    my_ip = subprocess.check_output(['curl', 'ifconfig.co'])
else: my_ip = find_ip_win()


main_canvas.create_text(200,50, text='Tic-Tac-Toe', justify=CENTER, font='Arial 14')
main_canvas.create_text(200, 100, text=my_ip, justify=CENTER, font='Arial 12', tag='conn')
main_canvas.create_text(200, 80, text='Your server IP:', justify=CENTER, font='Arial 10', tag='conn')
main_canvas.create_text(200, 140, text='Connect to:', justify=CENTER, font='Arial 10', tag='conn')

conadr = StringVar()
coninpt = Entry(main_canvas, width=30, textvariable=conadr)
#coninpt.insert(0, 'server')
coninpt_window = main_canvas.create_window(200,160, window=coninpt, tag='conn')

is_local = IntVar()
def change_state():
    if is_local.get():
        global conadr
        coninpt.config(state='disabled')
        conadr.set('localhost')
        #print('disabled')
    else:
        coninpt.config(state='normal')
check_local = Checkbutton(main_canvas, text='Local play', variable=is_local, command=change_state)
check_local_window = main_canvas.create_window(200, 190, window=check_local, tag='conn')
        

master.mainloop()

quit = False
while not quit:
    try:
        data_recv = sock.recv(1024)
        print(data_recv)
    except:
        print('Connection is off')
        quit = True
sock.close()
