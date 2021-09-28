from pynput import keyboard

class Action:
    def __init__(self, deserializeable):
        self.id = deserializeable['ability']
        self.action_type = deserializeable['type']
        self.cooldown = deserializeable['cooldown']
        self.incurs_gcd = deserializeable['incurs_gcd']
        self.last_use = 0

    def can_activate(self, activation_time):
        return activation_time - self.last_use > self.cooldown

    def activate(self, activation_time):
        if activation_time - self.last_use > self.cooldown:
            self.last_use = activation_time
            return True
        else:
            return False

    def __str__(self):
        return "{} : {}".format(self.id, self.action_type)


class MousebindAction:
    shape = (30,30)
    def __init__(self, mousebind_dict):
        self.action = mousebind_dict['ability']
        self.x1 = mousebind_dict['x']
        self.y1 = mousebind_dict['y']
        self.x2 = mousebind_dict['w']
        self.y2 = mousebind_dict['h']
        self.key = ((self.x1+self.x2)/2, (self.y1+self.y2)/2)
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
        ability['ability'] = self.action
        ability['x'] = self.x1
        ability['y'] = self.y1
        ability['w'] = self.x2
        ability['h'] = self.y2
        return ability

    def __str__(self):
        return "{} : ({},{})".format(self.action, *self.key)


class KeybindAction:
    modifier_keys = [keyboard.Key.alt, keyboard.Key.alt_r, keyboard.Key.alt_l, keyboard.Key.alt_gr, keyboard.Key.shift,
                     keyboard.Key.shift_r, keyboard.Key.shift_l, keyboard.Key.ctrl, keyboard.Key.ctrl_r, keyboard.Key.ctrl_l]
    modifier_key_map = {'shift':'shift', 'shift_r':'shift', 'alt_l':'alt', 'alt_gr':'alt', 'alt':'alt', 'ctrl':'ctrl',
                        'ctrl_l':'ctrl', 'ctrl_r':'ctrl'}
    special_key_map = {'key.f1':'f1', 'key.f2':'f2', 'key.f3':'f3', 'key.f4':'f4', 'key.f5':'f5', 'key.f6':'f6', 'key.f7':'f7',
                       'key.f8':'f8', 'key.f9':'f9', 'key.f10':'f10', 'key.f11':'f11', 'key.f12':'f12'}

    def __init__(self, keybind_dict):
        self.action = keybind_dict['ability']
        self.primary_key = keybind_dict['key'].casefold()
        if keybind_dict['modifier'] is None:
            self.modifier_key = None
            self.key = self.primary_key.casefold()
        else:
            self.modifier_key = keybind_dict['modifier'].casefold()
            self.key = self.primary_key + self.modifier_key
        
    def __lt__(self, other):
        if isinstance(other, KeybindAction):
            other = other.key
        elif not isinstance(other, tuple):
            return False
        else:
            other = other[0].casefold() if other[1] is None else "".join(other).casefold()
        if self.key < other:
            return True
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, KeybindAction):
            other = other.key
        elif not isinstance(other, tuple):
            return False
        else:
            other = other[0].casefold() if other[1] is None else "".join(other).casefole()
        return self.key == other

    def to_dict(self):
        return {'ability':self.action, 'key':self.primary_key, 'modifier':self.modifier_key}

    def __hash__(self):
        return self.key.__hash__()

    def __str__(self):
        return "{} : ({} + {})".format(self.action, self.primary_key, self.modifier_key)
    

class ActionProfile:
    def __init__(self, profile_dict):
        self._keybinds = {}
        self._mousebinds = []

        for keybind in profile_dict['keypress_activated']:
            keybind_action = KeybindAction(keybind)
            self._keybinds[keybind_action.__hash__()] = keybind_action

        for mousebind in profile_dict['mouse_activated']:
            self._mousebinds.append(MousebindAction(mousebind))
        self._mousebinds.sort()

    def search_mousebind(self, key):
        first_index = 0
        last_index = len(self._mousebinds) - 1
        index = -1
        while first_index <= last_index and index == -1:
            middle_index = (first_index + last_index)//2
            if self._mousebinds[middle_index] == key:
                return self._mousebinds[middle_index]
            elif self._mousebinds[middle_index] < key:
                first_index = middle_index + 1
            else:
                last_index = middle_index - 1
        return None

    def search_keybind(self, key):
        key = key[0].casefold() if key[1] is None else "".join(key).casefold()
        try:
            return self._keybinds[key.__hash__()]
        except KeyError:
            return None

