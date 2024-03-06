import pygame
import random
import time
import sys
import importlib
import builtins

#initialize pygame window and global variables
pygame.init()
pygame.display.set_caption("Simulation")
w = 106
h = 80
dx = 12
dy = 12
screen = pygame.display.set_mode((w*dx,h*dy))
builtins.updated = [[],[]]

def draw(sphere):
    while len(updated[sphere]) > 0:
        x = updated[sphere][0][0]
        y = updated[sphere][0][1]
        color = updated[sphere][0][2]
        screen.fill(color,(x*dx,y*dy,dx,dy))
        updated[sphere].pop(0)

def main():
    # initialize variables
    last_tick = 0
    draw_sphere = 0
    sleep_time = 1
    sleeps = (0, 0.1, 0.25, 0.5, 1, float("inf"))

    # initialize game object, print directions
    life_class = getattr(importlib.import_module(sys.argv[1]), sys.argv[1])
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
                    draw_sphere = (draw_sphere + 1) % 2
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
            continue
        break


if __name__ == "__main__":
    main()
