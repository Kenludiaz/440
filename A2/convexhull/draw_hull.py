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


def add_point(event):
    draw_point(w, event.x, event.y)
    points.append((event.x, event.y))
    return


def draw_hull():
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

    # points = [(1356621356, 1536730951), (356718641, 1746555946), (825800549, 1783940602), (2788324663, 576040383), (1513016989, 2409728621), (1678050503, 1764187625), (1232303581, 3735281464)]

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
