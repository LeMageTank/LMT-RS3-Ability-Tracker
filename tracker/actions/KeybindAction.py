from pynput import keyboard

class KeybindAction:
    modifier_keys = [keyboard.Key.alt, keyboard.Key.alt_r, keyboard.Key.alt_l, keyboard.Key.alt_gr, keyboard.Key.shift,
                     keyboard.Key.shift_r, keyboard.Key.shift_l, keyboard.Key.ctrl, keyboard.Key.ctrl_r, keyboard.Key.ctrl_l]
    modifier_key_map = {'shift':'shift', 'shift_r':'shift', 'alt_l':'alt', 'alt_gr':'alt', 'alt':'alt', 'ctrl':'ctrl',
                        'ctrl_l':'ctrl', 'ctrl_r':'ctrl'}
    special_key_map = {'key.f1':'f1', 'key.f2':'f2', 'key.f3':'f3', 'key.f4':'f4', 'key.f5':'f5', 'key.f6':'f6', 'key.f7':'f7',
                       'key.f8':'f8', 'key.f9':'f9', 'key.f10':'f10', 'key.f11':'f11', 'key.f12':'f12', 'À':'`', '½':'-',
                       '»':'=', 'Û':'[', 'Ý':']', 'Ü':'\\', 'º':';', 'Þ':'\'', '¼':',', '¾':'.', '¿':'/', 'key.backspace':'backspace',
                       'key.tab':'tab', 'key.caps_lock':'caps lock', 'key.esc':'esc', 'key.delete':'delete', 'key.left':'left',
                       'key.up':'up', 'key.down':'down', 'key.right':'right'}
    modifier_keys_strings = ['', 'alt', 'shift', 'ctrl']

    def __init__(self, keybind_dict):
        self.primary_key = keybind_dict['key'].casefold()
        self.actions = []
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
        return {'key':self.primary_key, 'modifier':self.modifier_key}

    def __hash__(self):
        return self.key.__hash__()

    def __str__(self):
        return "({} + {})".format(self.primary_key, self.modifier_key)
