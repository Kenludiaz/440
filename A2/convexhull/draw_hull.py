import copy
import time
from tkinter import Button
from tkinter import Canvas
from tkinter import NORMAL
from tkinter import PhotoImage
from tkinter import Tk

from convex_hull import compute_hull


def draw_point(canvas, x, y):
    return canvas.create_image((x, y), image=point_img, state=NORMAL)

def draw_text(canvas, x, y):
    return canvas.create_text(x + 50, y + 50,fill="darkblue",font="Times 20 italic bold",
                        text=f'({x},{y})')


def add_point(event):
    draw_point(w, event.x, event.y)
    draw_text(w, event.x, event.y)
    points.append((event.x, event.y))
    return


def draw_hull():
    # points = [(183, 117), (210, 249), (260, 434), (344, 616), (354, 645), (465, 266), (470, 92), (495, 516), (533, 464), (701, 353), (715, 241), (784, 643), (809, 526)]
    hull = copy.copy(compute_hull(points))
    hull.append(hull[0])
    for i in range(0, len(hull) - 1):
        x1 = hull[i][0]
        y1 = hull[i][1]
        x2 = hull[i + 1][0]
        y2 = hull[i + 1][1]
        w.create_line(x1, y1, x2, y2, width=3)
    return


if __name__ == '__main__':
    master, points = Tk(), list()

    submit_button = Button(master, text="Draw Hull", command=draw_hull)
    submit_button.pack()
    quit_button = Button(master, text="Quit", command=master.quit)
    quit_button.pack()


    canvas_width = 1000
    canvas_height = 800
    w = Canvas(master,
               width=canvas_width,
               height=canvas_height)
    point_img = PhotoImage(file="ram-sm-bl.gif")
    w.pack()
    w.bind('<Button-1>', add_point)

    w.mainloop()
