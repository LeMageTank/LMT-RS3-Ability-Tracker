from tracker.util.Constants import *
from tracker.actions.KeybindAction import KeybindAction
from tracker.actions.MousebindAction import MousebindAction

class ActionBar:
    def __init__(self, name, slots):
        self.name = name
        self.keybinds = [None for i in range(NUM_ACTIONS_SLOTS_PER_ACTION_BAR)]
        self.mousebinds = [None for i in range(NUM_ACTIONS_SLOTS_PER_ACTION_BAR)]
        for i in range(len(slots)):
            self.keybinds[i] = KeybindAction(slots[i]['keybind'])
            self.mousebinds[i] = MousebindAction.from_dict(slots[i]['mousebind'])

    def load_preset(self, preset):
        for i in range(len(self.keybinds)):
            self.keybinds[i].actions = preset[i]
            self.mousebinds[i].actions = preset[i]
