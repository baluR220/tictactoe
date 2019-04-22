import socket, subprocess, sys 
from tkinter import *

#server = '109.233.239.229'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

conadr = StringVar()
main_canvas.create_text(200,50, text='Tic-Tac-Toe', justify=CENTER, font='Arial 14')

count = 0
def draw_field():
    main_canvas.create_line(150,100,150,400, fill='black', tag='field')
    main_canvas.create_line(250,100,250,400, fill='black', tag='field')
    main_canvas.create_line(50,200,350,200, fill='black', tag='field')
    main_canvas.create_line(50,300,350,300, fill='black', tag='field')
    main_canvas.create_text(200,450, text='Press Space to restart', justify=CENTER, font='Arial 14', tag='field')
    back_button = Button(main_canvas, text='Back', command=menu, bg='white')
    back_window = main_canvas.create_window(380,20, window=back_button, tag='field')
 
def draw_cross(x,y):
    main_canvas.create_polygon(x-10,y,x-40,y-30,x-30,y-40,
                     x,y-10,x+30,y-40,x+40,y-30,
                     x+10,y,x+40,y+30,x+30,y+40,
                     x,y+10,x-30,y+40,x-40,y+30, fill='red',tag='figure')
    
def draw_circle(x,y):
    main_canvas.create_oval(x-40,y-40,x+40,y+40, fill='blue',tag='figure')
    main_canvas.create_oval(x-30,y-30,x+30,y+30, fill='white',tag='figure')

def draw(event):
    x,y = event.x, event.y
    global count, dest
    if conadr.get() != 'localhost':
        if count == 1:
            draw_cross(x,y)
            count = 0
        else:
            draw_circle(x,y)
            count = 1
    sock.sendto((str(x)+'_'+str(y)+str(count)).encode(), dest)

def draw_con(data): 
    global count
    count = int(data[-1:])
    #print(count)
    x = int(data[:data.find('_')])
    #print(x)
    y = int(data[data.find('_')+1:-1])
    #print(y)
    if count == 1:
        draw_cross(x,y)
        count = 0
    else:
        draw_circle(x,y)
        count = 1

def restart(event):
    global count
    count = 0
    main_canvas.delete('figure')
    sock.sendto('restart'.encode(), dest)

def main():
    global dest
    if conadr.get()=='localhost':
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(('', 9090))
        dest = ('255.255.255.255', 9090)
        print('local is on')
    else:
        dest = (conadr.get(), 11719)
        try:
            sock.sendto(('Hello').encode(), dest)
            print('Connection is on')
        except:
            print('Incorrect address')
    main_canvas.delete('conn')
    draw_field()
    main_canvas.focus_set()
    main_canvas.bind('<Button-1>', draw)
    main_canvas.bind('<space>', restart)

    def loopproc():
        sock.setblocking(False)
        try:
            data = sock.recv(1024).decode()
            #print(data)
            if data=='restart':
                main_canvas.delete('figure')
            else:
                draw_con(data)
        except:
            master.after(1,loopproc)
            return
        master.after(1,loopproc)
        return
    master.after(1,loopproc)


def menu():
    global my_ip
    main_canvas.delete('field')
    restart()
    main_canvas.create_text(200, 100, text=my_ip, justify=CENTER, font='Arial 12', tag='conn')
    main_canvas.create_text(200, 80, text='Your server IP:', justify=CENTER, font='Arial 10', tag='conn')
    main_canvas.create_text(200, 140, text='Connect to:', justify=CENTER, font='Arial 10', tag='conn')


    coninpt = Entry(main_canvas, width=30, textvariable=conadr)
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
            conadr.set('')
    check_local = Checkbutton(main_canvas, text='Local play', variable=is_local, command=change_state, bg='white')
    check_local_window = main_canvas.create_window(200, 190, window=check_local, tag='conn')
    conb = Button(main_canvas, text='Start', command=main, bg='white')
    conb_window = main_canvas.create_window(200,400, window=conb, tag='conn')
menu()
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
