import pygame
import random
import time

#initialize pygame widow and global variables
pygame.init()
pygame.display.set_caption("GameOfLife")
w = 1200
h = 960
screen = pygame.display.set_mode((w,h))
last_tick = 0
sleep_time = 0
sleeps = (0, 0.1, 0.25, 0.5, 1, float("inf"))

class GameOfLife:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.dx = 12
        self.dy = 12
        
        # intialize cells
        # 50/50 chance to start alive or dead
        self.cells = [[0 for y in range(self.h)] for x in range(self.w)]
        for x in range(self.w):
            for y in range(self.h):
                if random.random() < 0.5:
                    screen.fill((0,255,0),(x*self.dx,y*self.dy,self.dx,self.dy))
                    self.cells[x][y] = 1
                else:
                    screen.fill((0,0,0),(x*self.dx,y*self.dy,self.dx,self.dy))
                    self.cells[x][y] = 0

    def tick(self):
        # prepare a new array for updates so tick is global
        new_cells = [[0 for y in range(self.h)] for x in range(self.w)]
        
        for x in range(0,self.w):
            for y in range(0,self.h):
                cell = self.cells[x][y]
                # count neighbors, not including self
                neighbors = 0 - cell
                for i in range(-1,2):
                    for j in range(-1,2):
                        neighbors += self.cells[(x+i+self.w) % self.w][(y+j+self.h) % self.h]
                
                if (cell == 0 and neighbors == 3) or (cell == 1 and (neighbors == 2 or neighbors == 3)):
                    new_cells[x][y] = 1
                    screen.fill((0,255,0),(x*self.dx,y*self.dy,self.dx,self.dy))
                else:
                    new_cells[x][y] = 0
                    screen.fill((0,0,0),(x*self.dx,y*self.dy,self.dx,self.dy))
        
        # keep updated array
        self.cells = new_cells
    
    def flip(self, pos):
        # find cell by integer dividing click position by cell size
        x = pos[0] // self.dx
        y = pos[1] // self.dy
        # inline XOR, 0 becomes 1, 1 becomes 0
        self.cells[x][y] ^= 1
        screen.fill((0,255*self.cells[x][y],0),(x*self.dx,y*self.dy,self.dx,self.dy))

# initialize game object, print directions
life = GameOfLife(100, 80)
print("Mouse click to toggle cells")
print("Left/Right arrows to control tick rate")
    
while 1:
    # tick after waiting sleep_time seconds
    if time.time() >= last_tick + sleeps[sleep_time]:
        life.tick()
        print((time.time()-last_tick)*1000)
        last_tick = time.time()
    
    # handle each event
    for event in pygame.event.get():
        # handle time changes
        # possible wait times are pulled from a global list
        # max FPS, 10 FPS, 4 FPS, 2 FPS, 1 FPS, frozen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                sleep_time = max(sleep_time - 1, 0)
            if event.key == pygame.K_RIGHT:
                sleep_time = min(sleep_time + 1, 5)
        
        # handle click
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            life.flip(pos)

        #handle quit
        if event.type == pygame.QUIT:
            # exit the main loop
            print("should quit")
            break
    else: 
        pygame.display.flip()
        continue
    break