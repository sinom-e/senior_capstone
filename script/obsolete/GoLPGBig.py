import pygame
import random
import time

pygame.init()
pygame.display.set_caption("GameOfLife")
w = 400
h = 320
screen = pygame.display.set_mode((w,h))
color_dict = {0: "black", 1: "green"}
last_draw = 0
ticks = 0

class GameOfLife:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.dx = 1
        self.dy = 1
        
        self.map = [[0 for y in range(self.h)] for self.w in range(w)]
        self.cells = [[0 for y in range(self.h)] for self.w in range(w)]
        for x in range(self.w):
            for y in range(self.h):
                if random.random() < 0.5:
                    screen.fill((0,255,0),(x*self.dx,y*self.dy,self.dx,self.dy))
                    self.cells[x][y] = 1
                else:
                    screen.fill((0,0,0),(x*self.dx,y*self.dy,self.dx,self.dy))
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
                    screen.fill((0,255,0),(x*self.dx,y*self.dy,self.dx,self.dy))
                    new_cells[x][y] = 1
                else:
                    screen.fill((0,0,0),(x*self.dx,y*self.dy,self.dx,self.dy))
                    new_cells[x][y] = 0
        
        self.cells = new_cells

life = GameOfLife(400, 320)

while 1:
    life.tick()
    ticks = ticks+1

    if time.time() >= last_draw + 1:
        last_draw = time.time()
        print(ticks)
        ticks = 0
    
    pygame.display.flip()
    for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # exit the main loop
                print("should quit")
                break
    else: 
        continue
    break
    # time.sleep(0.01)