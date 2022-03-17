class MousebindAction:
    shape = (30,30)
    def __init__(self, mousebind_dict):
        self.action = mousebind_dict['action']
        self.x1 = mousebind_dict['x1']
        self.y1 = mousebind_dict['y1']
        self.x2 = mousebind_dict['x2']
        self.y2 = mousebind_dict['y2']
        self.key = ((self.x1+self.x2)/2, (self.y1+self.y2)/2)
        self.image = None
            #      y1
            #   x1    x2
            #      y2

    def __lt__(self, other):
        if isinstance(other, MousebindAction):
            other = other.key
        elif not isinstance(other, tuple):
            return False
        if self.x2 < other[0]:
            return True
        elif self.x1 <= other[0]:
            return other[1] < self.y2
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, MousebindAction):
            other = other.key
        elif not isinstance(other, tuple):
            return False
        return abs(other[0]-self.key[0]) <= self.shape[0]/2 and abs(other[1]-self.key[1]) <= self.shape[1]/2

    def box(self):
        return [self.x1, self.y1,
                self.x2, self.y1,
                self.x2, self.y2,
                self.x1, self.y2,
                self.x1, self.y1]

    def to_dict(self):
        ability = {}
        ability['action'] = self.action
        ability['x1'] = self.x1
        ability['y1'] = self.y1
        ability['x2'] = self.x2
        ability['y2'] = self.y2
        return ability

    def __str__(self):
        return "{} : ({},{})".format(self.action, *self.key)

