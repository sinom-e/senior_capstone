updated = []

class Simulation:
    def __init__(self):
        pass

    def tick(self):
        pass
    
    def draw(self):
        pass
    
    def on_click(self, pos):
        pass
    
    def _neighbors(sphere, x, y, cell_type):
        return (cell_at(sphere, x-1, y-1) == cell_type \
        + cell_at(sphere, x, y-1) == cell_type \
        + cell_at(sphere, x+1, y-1) == cell_type \
        + cell_at(sphere, x-1, y) == cell_type \
        + cell_at(sphere, x+1, y) == cell_type \
        + cell_at(sphere, x-1, y+1) == cell_type \
        + cell_at(sphere, x, y+1) == cell_type \
        + cell_at(sphere, x+1, y+1) == cell_type)
        
        for i in range(-1,2):
            for j in range(-1,2):
                neighbors += self.cells[(x+i+self._w) % self._w][(y+j+self._h) % self._h]
    
    def cell_at(sphere, x, y):
        return self.cells[(x+i+self._w) % self._w][(y+j+self._h) % self._h]

class GameOfLife(Simulation):
    def __init__(self, w, h):
        _w = w
        _h = h
        _dx = 12
        _dy = 12
        
        _spheres = [[[0 for y in range(self._h)] for x in range(self._w)]]
        for x in range(self._w):
            for y in range(self._h):
                if random.random() < 0.5:
                    self._spheres[0][x][y] = 1
                else:
                    self._spheres[0][x][y] = 0
    
    def tick(self):
        # prepare a new array for updates so tick is global
        new_cells = [[0 for y in range(self._h)] for x in range(self._w)]
        
        for x in range(0,self._w):
            for y in range(0,self._h):
                cell_type = self._spheres[0][x][y]
                # count neighbors, not including self
                match cell_type:
                    case 0:
                        if self._neighbors(0, x, y, 1) == 3:
                            new_cells[x][y] = 1
                            updated.push((x,y))
                    case 1:
                        n = self._neighbors(0, x, y, 1)
                        if n > 3 or n < 2:
                            new_cells[x][y] = 0
                            updated.push((x,y))
        
        # keep updated array
        self._spheres[0] = new_cells
    
    def draw(self):
        pass
    
    def on_click(self, pos):
        pass

spheres = []
text_file = open("new 3.txt", "r")
lines = text_file.readlines()
print(lines)
print(len(lines))
for line in lines:
    commands = line.replace('\n','').split(' ')
    print(commands)
    match commands[0]:
        case '!':
            spheres.append(Sphere(int(commands[1]), int(commands[2])))
        case _:
            spheres[int(commands[0])].set_tree(int(commands[1]), commands.pop(0).pop(0))
text_file.close()