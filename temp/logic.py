from tkinter import *

master = Tk()
main_canvas = Canvas(master, width=400, height=500, bg='white')
main_canvas.pack()

main_canvas.create_text(200, 50, text='Tic-Tac-Toe',
                        justify=CENTER, font='Arial 14')
count = 0
free_mode = 0
moves = [9 for i in range(9)]

normal_coords = [[0, 150, 0, 200, 100, 150, 0],
                 [150, 250, 0, 200, 200, 150, 1],
                 [250, 400, 0, 200, 300, 150, 2],
                 [0, 150, 200, 300, 100, 250, 3],
                 [150, 250, 200, 300, 200, 250, 4],
                 [250, 400, 200, 300, 300, 250, 5],
                 [0, 150, 300, 500, 100, 350, 6],
                 [150, 250, 300, 500, 200, 350, 7],
                 [250, 400, 300, 500, 300, 350, 8]]


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


def draw(event):
    global count
    x, y = event.x, event.y
    if not free_mode:
        x, y, cage = normalize(x, y)
        print(cage)
        last_form = watch_moves(x, y, count, cage)
    if count == 1:
        draw_cross(x, y)
        count = 0
    elif count == 0:
        draw_circle(x, y)
        count = 1
    else:
        count = last_form

def draw_field():
    main_canvas.create_line(150, 100, 150, 400, fill='black')
    main_canvas.create_line(250, 100, 250, 400, fill='black')
    main_canvas.create_line(50, 200, 350, 200, fill='black')
    main_canvas.create_line(50, 300, 350, 300, fill='black')
    main_canvas.create_text(
        200, 450, text='Press Space to restart', justify=CENTER, font='Arial 14')


def draw_cross(x, y):
    main_canvas.create_polygon(x - 10, y, x - 40, y - 30, x - 30, y - 40,
                               x, y - 10, x + 30, y - 40, x + 40, y - 30,
                               x + 10, y, x + 40, y + 30, x + 30, y + 40,
                               x, y + 10, x - 30, y + 40, x - 40, y + 30, fill='red', tag='figure')


def draw_circle(x, y):
    main_canvas.create_oval(x - 40, y - 40, x + 40, y +
                            40, fill='blue', tag='figure')
    main_canvas.create_oval(x - 30, y - 30, x + 30, y +
                            30, fill='white', tag='figure')


def restart(event):
    global count, moves
    count = 0
    moves = [0 for i in range(8)]
    main_canvas.delete('figure')


def main():
    draw_field()
    main_canvas.focus_set()
    main_canvas.bind('<Button-1>', draw)
    main_canvas.bind('<space>', restart)


main()
master.mainloop()
