import pygame
import tkinter as tk
import os
import random
import time
import sys
import importlib
import builtins

#initialize pygame window and global variables
w = 106
h = 80
dx = 12
dy = 12
sleep_time = 1
sleeps = (0, 0.1, 0.25, 0.5, 1, float("inf"))

root = tk.Tk()
button_win = tk.Frame(root, width = h*dy, height = 25)
button_win.pack(side = tk.TOP)
embed_pygame = tk.Frame(root, width = w*dx, height = h*dy)
embed_pygame.pack(side = tk.TOP)

os.environ['SDL_WINDOWID'] = str(embed_pygame.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
pygame.display.init()
screen = pygame.display.set_mode()
# pygame.display.set_caption("Simulation")
# screen = pygame.display.set_mode((w*dx,h*dy))
builtins.updated = []

def window_close():
    global root
    root.destroy()
    pygame.quit()
    sys.exit()

root.protocol("WM_DELETE_WINDOW", window_close)

def speed_up():
    global sleep_time
    sleep_time = max(sleep_time - 1, 0)

def slow_down():
    global sleep_time
    sleep_time = min(sleep_time + 1, 5)

speed_up_button = tk.Button(button_win, text = 'speed up',  command = speed_up)
speed_up_button.pack(side=tk.RIGHT)
slow_down_button = tk.Button(button_win, text = 'slow down',  command = slow_down)
slow_down_button.pack(side=tk.LEFT)

def draw(sphere):
    while len(updated[sphere]) > 0:
        x = updated[sphere][0][0]
        y = updated[sphere][0][1]
        color = updated[sphere][0][2]
        screen.fill(color,(x*dx,y*dy,dx,dy))
        updated[sphere].pop(0)
    
    for i in range(len(updated)):
        updated[i] = []

def main():
    # initialize variables
    last_tick = 0
    draw_sphere = 0
    global sleep_time
    global sleeps
    

    # initialize game object, print directions
    life_class = getattr(importlib.import_module(sys.argv[1]), sys.argv[1])
    builtins.updated = [[] for i in range(life_class.n_screens())]
    life = life_class(w, h, dx, dy) 
    
    while 1:
        # tick after waiting sleep_time seconds
        if time.time() >= last_tick + sleeps[sleep_time]:
            life.tick()
            # print((time.time()-last_tick)*1000)
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
                if event.key == pygame.K_d:
                    if life_class.n_screens() > 1:
                        draw_sphere = (draw_sphere + 1) % life_class.n_screens()
                        screen.fill((0,0,0))
        
            # handle click
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                life.on_click(pos)
            
            #handle quit
            if event.type == pygame.QUIT:
                # exit the main loop
                print("should quit")
                break

        else: 
            draw(draw_sphere)
            pygame.display.flip()
            root.update()
            continue


if __name__ == "__main__":
    main()
