from Simulation import Simulation
import builtins
import random

class Forage(Simulation):
    def __init__(self, w, h, dx, dy):
        self._w = w
        self._h = h
        self._dx = dx
        self._dy = dy
        
        self._spheres = []
        self._spheres.append([[0 for y in range(self._h)] for x in range(self._w)])
        self._spheres.append([[0 for y in range(self._h)] for x in range(self._w)])
        self._spheres.append([[0 for y in range(self._h)] for x in range(self._w)])
        
        self._colors = [[(0,0,0),(0,255,0)],[],[(0,0,0),(255,0,0)]]
        
        for x in range(self._w):
            for y in range(self._h):
                if random.random() < 0.001:
                    self._spheres[1][x][y] = 1
                    builtins.updated[0].append((x,y,self._colors[2][1]))
                else:
                    self._spheres[1][x][y] = 0
                    builtins.updated[0].append((x,y,self._colors[0][0]))
    
    def tick(self):
        ground = self._spheres[0]
        animal = self._spheres[1]
        scents = self._spheres[2]
        
        # animals first pass
        for y in range(0,self._h):
            for x in range(0,self._w):
                cell_type = animal[x][y]
                match cell_type:
                    case 0:
                        # no animal
                        pass
                    
                    case 1:
                        # leave animal scent
                        scents[x][y] = -1
                        
                        # move toward strongest scent
                        dirs = [(x+1,y), (x+1,y+1), (x+1,y-1), (x,y+1), (x,y-1), (x-1,y), (x-1,y+1), (x-1,y-1)]
                        
                        random.shuffle(dirs)
                        dirs.sort(key=lambda dir_tup: self.get_cell(2, dir_tup[0], dir_tup[1]) * -1)
                        
                        ex = x
                        ey = y
                        
                        while len(dirs):
                            if self.get_cell(1, dirs[0][0], dirs[0][1]) == 0:
                                ex = dirs[0][0]
                                ey = dirs[0][1]
                                builtins.updated[0].append((x,y,self._colors[0][0]))
                                break
                            
                            dirs.pop(0)
                        
                        self.set_cell(1, x, y, 0)
                        self.set_cell(1, ex, ey, 2)
                        
                        builtins.updated[0].append((ex,ey,self._colors[2][1]))
        
        # animals second pass
        for y in range(0,self._h):
            for x in range(0,self._w):
                cell_type = animal[x][y]
                match cell_type:
                    case 2:
                        animal[x][y] = 1
        
        # ground
        for y in range(0,self._h):
            for x in range(0,self._w):
                cell_type = ground[x][y]
                match cell_type:
                    case 0:
                        # grow a flower
                        if random.random() < 0.00001:
                            ground[x][y] = 1
                    case 1:
                        # produce scent in cell
                        scents[x][y] = 1
                        
                        # get eaten
                        if animal[x][y] != 0:
                            ground[x][y] = 0
                        else:
                            builtins.updated[0].append((x,y,self._colors[0][1]))
        
        # scents
        new_scents = [[0 for y in range(self._h)] for x in range(self._w)]
        for y in range(0,self._h):
            for x in range(0,self._w):
                new_scents[x][y] = (self._sum(2, x, y) / 9) - 0.001
                builtins.updated[1].append((x,y,(min(max(new_scents[x][y]*128+128,0),255),min(max(new_scents[x][y]*128+128,0),255),min(max(new_scents[x][y]*128+128,0),255))))
        
        self._spheres[2] = new_scents
    
    def on_click(self, pos):
        # find cell by integer dividing click position by cell size
        x = pos[0] // self._dx
        y = pos[1] // self._dy
        # plant flower
        self._spheres[0][x][y] = 1
        builtins.updated[0].append((x,y,self._colors[0][1]))

    @staticmethod
    def n_screens():
        return 2