class Simulation:
    _parameters = []
    _spheres = []
    _colors = []
    _screens = 0
    _w = 0
    _h = 0
    _dx = 0
    _dy = 0
    
    def __init__(self):
        pass

    def tick(self):
        pass
    
    def on_click(self, pos):
        pass
    
    def _neighbors(self, sphere, x, y, cell_type):
        return int(self.get_cell(sphere, x-1, y-1) == cell_type) \
        + int(self.get_cell(sphere, x, y-1) == cell_type) \
        + int(self.get_cell(sphere, x+1, y-1) == cell_type) \
        + int(self.get_cell(sphere, x-1, y) == cell_type) \
        + int(self.get_cell(sphere, x+1, y) == cell_type) \
        + int(self.get_cell(sphere, x-1, y+1) == cell_type) \
        + int(self.get_cell(sphere, x, y+1) == cell_type) \
        + int(self.get_cell(sphere, x+1, y+1) == cell_type)
    
    def _sum(self, sphere, x, y):
        return self.get_cell(sphere, x-1, y-1) \
        + self.get_cell(sphere, x, y-1) \
        + self.get_cell(sphere, x+1, y-1) \
        + self.get_cell(sphere, x-1, y) \
        + self.get_cell(sphere, x+1, y) \
        + self.get_cell(sphere, x-1, y+1) \
        + self.get_cell(sphere, x, y+1) \
        + self.get_cell(sphere, x+1, y+1) \
        + self.get_cell(sphere, x, y)
    
    def get_cell(self, sphere, x, y):
        return self._spheres[sphere][(x+self._w) % self._w][(y+self._h) % self._h]
    
    def set_cell(self, sphere, x, y, cell_type):
        self._spheres[sphere][(x+self._w) % self._w][(y+self._h) % self._h] = cell_type
    
    def get_sphere(self, sphere):
        return self._spheres[sphere]
    
    def get_color(self, cell_type):
        return self._colors[cell_type]
    
    def n_parameters(self):
        return len(self._parameters)
    
    def get_parameter(self, parameter):
        #parameter structure: 0:label 1:value 2:from 3:to 4:resolution
        return self._parameters[parameter]
    
    def set_parameter(self, parameter, value):
        self._parameters[parameter][1] = value
    
    @staticmethod
    def n_screens():
        return 1