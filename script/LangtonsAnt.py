from Simulation import Simulation
import builtins

class LangtonsAnt(Simulation):
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
        
        self._spheres.append([[0 for y in range(self._h)] for x in range(self._w)])
        
        self._colors = [[(0,0,0),(255,255,255)]]
    
    def tick(self):
        if self._spheres[0][self._ant_x][self._ant_y] == 0:
            self._spheres[0][self._ant_x][self._ant_y] = 1
            builtins.updated[0].append((self._ant_x,self._ant_y,self._colors[0][1]))
            self._ant_dir = (self._ant_dir+3) % 4
        else:
            self._spheres[0][self._ant_x][self._ant_y] = 0
            builtins.updated[0].append((self._ant_x,self._ant_y,self._colors[0][0]))
            self._ant_dir = (self._ant_dir+1) % 4
        
        match self._ant_dir:
            case 0:
                self._ant_y = (self._ant_y-1+self._h) % self._h
            case 1:
                self._ant_x = (self._ant_x-1+self._w) % self._w
            case 2:
                self._ant_y = (self._ant_y+1+self._h) % self._h
            case 3:
                self._ant_x = (self._ant_x+1+self._w) % self._w
        
        builtins.updated[0].append((self._ant_x,self._ant_y,(0,0,255)))
    
    def on_click(self, pos):
        # find cell by integer dividing click position by cell size
        x = pos[0] // self._dx
        y = pos[1] // self._dy
        # inline XOR, 0 becomes 1, 1 becomes 0
        builtins.updated[0].append((self._ant_x,self._ant_y,(255,0,0)))
        self._ant_x = x
        self._ant_y = y
        builtins.updated[0].append((self._ant_x,self._ant_y,(255,0,0)))