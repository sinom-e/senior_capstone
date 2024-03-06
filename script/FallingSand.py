from Simulation import Simulation
import builtins
import random

class FallingSand(Simulation):
    _ant_x = 0
    _ant_y = 0
    _ant_dir = 0
    
    def __init__(self, w, h, dx, dy):
        self._w = w
        self._h = h
        self._dx = dx
        self._dy = dy
        
        self._ant_x = self._w // 2
        self._ant_y = h // 2
        
        self._colors = [[(0,0,0),(255,255,0),(127,127,127)]]
        
        self._spheres.append([[0 for y in range(self._h)] for x in range(self._w)])
        for x in range(self._w):
            for y in range(self._h):
                if random.random() < 0.1:
                    self._spheres[0][x][y] = 1
                    builtins.updated[0].append((x,y,self._colors[0][1]))
                else:
                    self._spheres[0][x][y] = 0
    
    def tick(self):
	    # prepare a new array for updates so tick is global
        new_cells = [[0 for y in range(self._h)] for x in range(self._w)]
        sand = 0
        
        for y in reversed(range(0,self._h)):
            for x in range(0,self._w):
                cell_type = self._spheres[0][x][y]
                match cell_type:
                    case 1:
                        # count sand
                        sand = sand + 1
                        
                        if self.get_cell(0, x, y+1) == 0:
                            self.set_cell(0, x, y, 0)
                            self.set_cell(0, x, y+1, 1)
                            
                            builtins.updated[0].append((x,y,self._colors[0][0]))
                            builtins.updated[0].append((x,(y+1+self._h) % self._h,self._colors[0][1]))
                            
                        elif self.get_cell(0, x-1, y+1) == 0:
                            self.set_cell(0, x, y, 0)
                            self.set_cell(0, x-1, y+1, 1)
                            
                            builtins.updated[0].append((x,y,self._colors[0][0]))
                            builtins.updated[0].append(((x-1+self._w) % self._w,(y+1+self._h) % self._h,self._colors[0][1]))
                            
                        elif self.get_cell(0, x+1, y+1) == 0:
                            self.set_cell(0, x, y, 0)
                            self.set_cell(0, x+1, y+1, 1)
                            
                            builtins.updated[0].append((x,y,self._colors[0][0]))
                            builtins.updated[0].append(((x+1+self._w) % self._w,(y+1+self._h) % self._h,self._colors[0][1]))
        
        print(sand)
    
    def on_click(self, pos):
        # find cell by integer dividing click position by cell size
        x = pos[0] // self._dx
        y = pos[1] // self._dy
        # inline XOR, 0 becomes 1, 1 becomes 0
        self._spheres[0][x][y] = 2
        builtins.updated[0].append((x,y,self._colors[0][2]))
