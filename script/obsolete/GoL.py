from tkinter import *
import random
import time

tk = Tk()
tk.title = "GameOfLife"
tk.resizable(0,0)
tk.wm_attributes("-topmost", 1)
w = 500
h = 400
color_dict = {0: "black", 1: "green"}
last_draw = 0
ticks = 0

canvas = Canvas(tk, width=w, height=h, bd=0, highlightthickness=0)
canvas.pack()

class GameOfLife:
    def __init__(self, canvas, w, h):
        self.canvas = canvas
        self.w = w
        self.h = h
        self.dx = 10
        self.dy = 10
        
        self.map = [[0 for y in range(self.h)] for self.w in range(w)]
        self.cells = [[0 for y in range(self.h)] for self.w in range(w)]
        for x in range(self.w):
            for y in range(self.h):
                if random.random() < 0.5:
                    self.map[x][y] = self.canvas.create_rectangle(x * self.dx + 1, y * self.dy + 1, (x + 1) * self.dx, (y + 1) * self.dy, fill=color_dict[1], activeoutline='white')
                    self.cells[x][y] = 1
                else:
                    self.map[x][y] = self.canvas.create_rectangle(x * self.dx + 1, y * self.dy + 1, (x + 1) * self.dx, (y + 1) * self.dy, fill=color_dict[0], activeoutline='white')
                    self.cells[x][y] = 0

    def tick(self):
        new_cells = [[0 for y in range(self.h)] for x in range(self.w)]
        
        for x in range(1,self.w-1):
            for y in range(1,self.h-1):
                cell = self.cells[x][y]
                neighbors = 0 - cell
                for i in range(-1,2):
                    for j in range(-1,2):
                        neighbors += self.cells[x+i][y+j]
                
                if (cell == 0 and neighbors == 3) or (cell == 1 and (neighbors == 2 or neighbors == 3)):
                    new_cells[x][y] = 1
                else:
                    new_cells[x][y] = 0
        
        self.cells = new_cells
        
        for x in range(self.w):
            for y in range(self.h):
                self.canvas.itemconfig(self.map[x][y], fill=color_dict[self.cells[x][y]])

life = GameOfLife(canvas, 50, 40)

while 1:
    life.tick()
    tk.update_idletasks()
    tk.update()
    
    ticks = ticks+1

    if time.time() >= last_draw + 1:
        last_draw = time.time()
        print(ticks)
        ticks = 0
    
    # time.sleep(0.1)