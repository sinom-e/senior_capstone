from Simulation import Simulation
import builtins
import random

class ForestFire(Simulation):
    def __init__(self, w, h, dx, dy):
        self._w = w
        self._h = h
        self._dx = dx
        self._dy = dy
        
        #parameter structure: 0:label 1:value 2:from 3:to 4:resolution
        self._parameters = [['Grow Rate', 0.0001, 0, 0.01, 0.0001],['Fire Rate', 0.00001, 0, 0.001, 0.00001]]
        
        self._spheres = []
        self._spheres.append([[0 for y in range(self._h)] for x in range(self._w)])
        
        self._colors = [[(0,0,0),(0,255,0),(255,0,0)]]
    
    def tick(self):
        # prepare a new array for updates so tick is global
        new_cells = [[0 for y in range(self._h)] for x in range(self._w)]
        grow_rate = self._parameters[0][1]
        fire_rate = self._parameters[1][1]
        
        for x in range(0,self._w):
            for y in range(0,self._h):
                cell_type = self._spheres[0][x][y]
                # count neighbors, not including self
                match cell_type:
                    case 0:
                        if random.random() < grow_rate:
                            new_cells[x][y] = 1
                            builtins.updated[0].append((x,y,self._colors[0][1]))
                    case 1:
                        if self._neighbors(0, x, y, 2) > 0 or random.random() < fire_rate:
                            new_cells[x][y] = 2
                            builtins.updated[0].append((x,y,self._colors[0][2]))
                        else:
                            new_cells[x][y] = 1
                    case 2:
                        new_cells[x][y] = 0
                        builtins.updated[0].append((x,y,self._colors[0][0]))
        
        # keep updated array
        self._spheres[0] = new_cells
    
    def on_click(self, pos):
        # find cell by integer dividing click position by cell size
        x = pos[0] // self._dx
        y = pos[1] // self._dy
        # inline XOR, 0 becomes 1, 1 becomes 0
        self._spheres[0][x][y] = 2
        builtins.updated[0].append((x,y,self._colors[0][2]))