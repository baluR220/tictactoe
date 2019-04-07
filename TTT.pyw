from tkinter import *
import socket, subprocess, sys

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

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('0.0.0.0', 11719))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

master = Tk()
master.title('TTT_online')

w = Canvas(master, width=400, height=500, bg='white')
w.pack()
w.create_text(200,50, text='Tic-Tac-Toe', justify=CENTER, font='Arial 14')
w.create_text(200, 100, text=my_ip, justify=CENTER, font='Arial 12', tag='conn')
w.create_text(200, 80, text='Your IP:', justify=CENTER, font='Arial 10', tag='conn')
w.create_text(200, 140, text='Connect to:', justify=CENTER, font='Arial 10', tag='conn')

conadr = StringVar()
coninpt = Entry(w, width=30, textvariable=conadr)
coninpt_window = w.create_window(200,160, window=coninpt, tag='conn')


count = 0
def draw_field():
    w.create_line(150,100,150,400, fill='black')
    w.create_line(250,100,250,400, fill='black')
    w.create_line(50,200,350,200, fill='black')
    w.create_line(50,300,350,300, fill='black')
    w.create_text(200,450, text='Press Space to restart', justify=CENTER, font='Arial 14')
 
def draw_cross(x,y):
    w.create_polygon(x-10,y,x-40,y-30,x-30,y-40,
                     x,y-10,x+30,y-40,x+40,y-30,
                     x+10,y,x+40,y+30,x+30,y+40,
                     x,y+10,x-30,y+40,x-40,y+30, fill='red',tag='figure')
    
def draw_circle(x,y):
    w.create_oval(x-40,y-40,x+40,y+40, fill='blue',tag='figure')
    w.create_oval(x-30,y-30,x+30,y+30, fill='white',tag='figure')
   
def draw(event):
    x,y = event.x, event.y
    global count
    sock.sendto((str(x)+'_'+str(y)+str(count)).encode(), ('255.255.255.255', 11719))
    
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
    w.delete('figure')

def main():
    global conadr
    conadr = conadr.get()
    #print(conadr)
    w.delete('conn')
    draw_field()
    w.focus_set()    
    w.bind('<Button-1>', draw)
    w.bind('<space>', restart)


    def loopproc():
        s.setblocking(False)
        try:
            data = s.recv(128).decode()
            print(data)
            draw_con(data)
        except:
            master.after(1,loopproc)
            return
        master.after(1,loopproc)
        return
    master.after(1,loopproc)
    
conb = Button(w, text='Start', command=main)
conb_window = w.create_window(200,400, window=conb, tag='conn')

master.mainloop()
