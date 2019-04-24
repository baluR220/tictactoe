import socket, subprocess, sys 
from tkinter import *

count = 0
moves = [9 for i in range(9)]
win_seq = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
free_mode = 0
normal_coords = [[0, 150, 0, 200, 100, 150, 0],      #  [x1, x2, y1, y2, x, y, cage]
                 [150, 250, 0, 200, 200, 150, 1],    #   
                 [250, 400, 0, 200, 300, 150, 2],    #
                 [0, 150, 200, 300, 100, 250, 3],    #  (x1,y1)  _________ 
                 [150, 250, 200, 300, 200, 250, 4],  #           |       |    
                 [250, 400, 200, 300, 300, 250, 5],  #           | cage  | 
                 [0, 150, 300, 500, 100, 350, 6],    #           |_______|
                 [150, 250, 300, 500, 200, 350, 7],  #                     (x2,y2)
                 [250, 400, 300, 500, 300, 350, 8]]  #


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

def normalize(ix, iy):
    print(ix, iy)
    for line in normal_coords:
        if line[0] <= ix <= line[1] and line[2] <= iy <= line[3]:
            print(line[4], line[5])
            return(line[4], line[5], line[6])


def watch_moves(x, y, form, cage):
    global moves, count
    if moves[cage] == 9:
        moves[cage] = form
    else:
        count = 2
        return(form)
    print(moves)

def find_winner():
    global moves, win_seq, count
    winner = 'Draw.'
    for line in win_seq:
        if moves[line[0]] == moves[line[1]] == moves[line[2]] != 9:
            if moves[line[0]] == 0:
                winner = 'O is Winner!'
            if moves[line[0]] == 1:
                winner = 'X is Winner'
            main_canvas.create_rectangle(100,150,300,250, fill='white', tag='figure')
            main_canvas.create_text(200, 200, text=winner,
                        justify=CENTER, font='Arial 24', tag='figure', fill='red')
            for i in moves:
                if i == 9:
                    moves[moves.index(i)] = 2
        if 9 not in moves and winner == 'Draw.':
            main_canvas.create_text(200, 200, text=winner,
                        justify=CENTER, font='Arial 24', tag='figure', fill='red')

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
        global free_mode
        if not free_mode:
            x, y, cage = normalize(x, y)
            print(cage)
            last_form = watch_moves(x, y, count, cage)
            find_winner()
        if count == 1:
            draw_cross(x, y)
            count = 0
        elif count == 0:
            draw_circle(x, y)
            count = 1
        else:
            count = last_form
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
    global count, moves
    count = 0
    moves = [9 for i in range(9)]
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
    global my_ip, count, free_mode
    count = 0
    free_mode = 0
    main_canvas.unbind('<Button-1>')
    main_canvas.unbind('<space>')
    main_canvas.delete('field')
    main_canvas.delete('figure')
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
    is_free = IntVar()
    def change_mod():
        global free_mode
        free_mode = is_free.get()
        print(free_mode)
    check_free = Checkbutton(main_canvas, text='Free mod', variable=is_free,
        command=change_mod, bg='white')
    check_free_window = main_canvas.create_window(200, 210, window=check_free, tag='conn')
    
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
