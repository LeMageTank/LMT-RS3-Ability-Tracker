class MousebindAction:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.key = ((self.x1+self.x2)/2, (self.y1+self.y2)/2)
        self.shape = (self.x2 - self.x1, self.y2 - self.y1)
        self.actions = []

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
        
    def __hash__(self):
        return self.__str__().__hash__()

    def box(self):
        return [self.x1, self.y1,
                self.x2, self.y1,
                self.x2, self.y2,
                self.x1, self.y2,
                self.x1, self.y1]

    def coords(self):
        return (self.x1, self.y1, self.x2, self.y2)

    def to_dict(self):
        ability = {}
        ability['x1'] = self.x1
        ability['y1'] = self.y1
        ability['x2'] = self.x2
        ability['y2'] = self.y2
        return ability

    @classmethod
    def from_dict(self, mousebind_dict):
        if mousebind_dict is not None:
            return MousebindAction(mousebind_dict['x1'], mousebind_dict['y1'], mousebind_dict['x2'], mousebind_dict['y2'])
        else:
            return MousebindAction(-1, -1, -1, -1);

    def __str__(self):
        return '({},{})'.format(self.x1, self.y1)

