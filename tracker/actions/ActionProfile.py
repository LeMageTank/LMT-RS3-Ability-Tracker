from tracker.actions.KeybindAction import KeybindAction
from tracker.actions.MousebindAction import MousebindAction

class ActionProfile:
    def __init__(self, profile_dict, weapon_type):
        self._keybinds = {}
        self._mousebinds = []
        self._weapon_type = weapon_type
        self.weapon = None

        for keybind in profile_dict['keybinds']:
            keybind_action = KeybindAction(keybind)
            self._keybinds[keybind_action.__hash__()] = keybind_action

        for mousebind in profile_dict['mousebinds']:
            self._mousebinds.append(MousebindAction(mousebind))
        self._mousebinds.sort()

    @property
    def weapon_type(self):
        return self._weapon_type

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


