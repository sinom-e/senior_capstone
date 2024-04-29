import pygame
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os
import random
import time
import sys
import importlib
import builtins

import ui

#initialize pygame window and global variables
w = 100
h = 80
psize = 12
stopped = False
sleep_time = 1
sleeps = (0, 0.1, 0.25, 0.5, 1, 2.5, 5)
life_class = None
life = None
draw_sphere = 0

root = tk.Tk()
root.protocol( 'WM_DELETE_WINDOW' , root.destroy)

_top1 = root
_w1 = ui.Toplevel1(_top1)

embed_pygame = _w1.Frame1

os.environ['SDL_WINDOWID'] = str(embed_pygame.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
pygame.display.init()
screen = pygame.display.set_mode()
# pygame.display.set_caption("Simulation")
# screen = pygame.display.set_mode((w*psize,h*psize))
builtins.updated = []

def window_close():
    global root
    root.destroy()
    pygame.quit()
    sys.exit()

def speed_up():
    global sleep_time
    sleep_time = max(sleep_time - 1, 0)

def slow_down():
    global sleep_time
    sleep_time = min(sleep_time + 1, 5)
    
def stop_start():
    global stop_start_button
    global step_button
    global reset_button
    global stopped
    
    if stopped:
        stopped = False
        stop_start_button.configure(text = "Stop")
        step_button.configure(state = "disabled")
    else:
        stopped = True
        stop_start_button.configure(text = "Start")
        step_button.configure(state = "active")

def step():
    global life
    global draw_sphere
    global root
    
    life.tick()
    draw(draw_sphere)
    pygame.display.flip()
    root.update()

def draw(sphere):
    while len(updated[sphere]) > 0:
        x = updated[sphere][0][0]
        y = updated[sphere][0][1]
        color = updated[sphere][0][2]
        screen.fill(color,(x*psize,y*psize,psize,psize))
        updated[sphere].pop(0)
    
    for i in range(len(updated)):
        updated[i] = []

def init_sim():
    global root
    global _w1
    global width_box
    global height_box
    global life_class
    global life
    global w
    global h
    global psize
    
    screen.fill((0,0,0))
    
    w = int(float(width_box.get()))
    h = int(float(height_box.get()))
    psize = int(float(psize_box.get()))
    
    _w1.Frame1.place(x=190, y=10, width=w*psize, height=h*psize)
    root.geometry(str(200+w*psize)+'x'+str(max(20+h*psize,470)))
    
    life_class = getattr(importlib.import_module(sys.argv[1]), sys.argv[1])
    life = life_class(w, h, psize, psize) 
    builtins.updated = [[] for i in range(life_class.n_screens())]

reset_button = _w1.Button6
reset_button.configure(command = init_sim)

width_box = _w1.Spinbox1
height_box = _w1.Spinbox2
psize_box = _w1.Spinbox3

speed_up_button = _w1.Button3
speed_up_button.configure(command = speed_up)
slow_down_button = _w1.Button1
slow_down_button.configure(command = slow_down)

stop_start_button = _w1.Button4
stop_start_button.configure(command = stop_start)
step_button = _w1.Button2
step_button.configure(command = step)
    
def main():
    # initialize variables
    last_tick = 0
    global draw_sphere
    global sleep_time
    global sleeps
    global life_class
    global life
    global root
    global stopped

    # initialize game object, print directions
    init_sim()
    
    while 1:
        # tick after waiting sleep_time seconds
        if time.time() >= last_tick + sleeps[sleep_time] and not stopped:
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
