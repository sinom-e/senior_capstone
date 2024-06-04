import pygame
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import filedialog
from pathlib import Path
import os
import random
import time
import sys
import importlib
import builtins

import uitemp

#initialize pygame window and global variables
w = 100
h = 80
psize = 12
stopped = False
life_class_name = "GameOfLife"
life_class = None
life = None
draw_sphere = 0

root = tk.Tk()
root.protocol( 'WM_DELETE_WINDOW' , root.destroy)

_top1 = root
_w1 = uitemp.Toplevel1(_top1)

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

def update_params():
    global life
    global param_sliders
    
    for i in range(0,life.n_parameters()):
        life.set_parameter(i, param_sliders[i].get())

def step():
    global life
    global draw_sphere
    global root
    
    update_params()
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

def load_sim():
    global life_class_name
    old_life_class_name = life_class_name
    
    try:
        file_path = tk.filedialog.askopenfilename(filetypes=(("Simulation Script", "*.py"),), initialdir = sys.path[0])
    
        life_class_name = Path(file_path).stem
    
        init_sim()
    except:
        print("Invalid simulation file")
        life_class_name = old_life_class_name
        
        init_sim()

def init_sim():
    global root
    global _w1
    global width_box
    global height_box
    global param_sliders
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
    
    life_class = getattr(importlib.import_module(life_class_name), life_class_name)
    builtins.updated = [[] for i in range(life_class.n_screens())]
    life = life_class(w, h, psize, psize) 
    
    for i in range(0,life.n_parameters()):
        param = life.get_parameter(i)
        
        #parameter structure: 0:label 1:value 2:from 3:to 4:resolution
        param_sliders[i].configure(label = param[0], from_ = param[2], to = param[3], resolution = param[4])
        param_sliders[i].set(param[1])
    
    root.geometry(str(200+w*psize)+'x'+str(max( max(20+h*psize,380), 380+70*life.n_parameters() )))
    _w1.Controls.place(height = 115+70*life.n_parameters())
    
    draw(draw_sphere)
    pygame.display.flip()
    root.update()

def next_layer():
    global draw_sphere
    global life_class
    global life
    
    if life_class.n_screens() > 1:
        draw_sphere = (draw_sphere + 1) % life_class.n_screens()
        screen.fill((0,0,0))

load_button = _w1.Button5
load_button.configure(command = load_sim)

reset_button = _w1.Button6
reset_button.configure(command = init_sim)

width_box = _w1.Spinbox1
height_box = _w1.Spinbox2
psize_box = _w1.Spinbox3

delay_slider = _w1.FrameScale

stop_start_button = _w1.Button4
stop_start_button.configure(command = stop_start)
step_button = _w1.Button2
step_button.configure(command = step)

layer_button = _w1.Button1_1
layer_button.configure(command = next_layer)

param_sliders = [_w1.parameter_0, _w1.parameter_1, _w1.parameter_2, _w1.parameter_3, _w1.parameter_4]
    
def main():
    # initialize variables
    last_tick = 0
    global draw_sphere
    global life_class
    global life
    global root
    global stopped
    global delay_slider

    # initialize game object, print directions
    init_sim()
    
    while 1:
        # tick after waiting sleep_time seconds
        if time.time() >= last_tick + delay_slider.get()/1000 and not stopped:
            update_params()
            life.tick()
            # print((time.time()-last_tick)*1000)
            last_tick = time.time()
    
        # handle each event
        for event in pygame.event.get():
            # handle time changes
            # possible wait times are pulled from a global list
            # max FPS, 10 FPS, 4 FPS, 2 FPS, 1 FPS, frozen
            if event.type == pygame.KEYDOWN:
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
