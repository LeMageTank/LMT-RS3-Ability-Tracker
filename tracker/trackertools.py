import pyautogui
import tkinter
import math
import time

# configuration: A dict of the config.json file in the root directory.
# action_profile: The user's loaded input profile.
# action_map: The dict containing every ability/action in the abilityinfo.json
#               file, including cooldowns, damage, etc.
# actions: The actions detected by the tracker since the last call to this object.
# global_cooldown: Time remaining until the end of the global cooldown [0 s., 1.8 s.]
# player_state: A dict containing the current state of the player.
class TrackerTool:
    def __init__(self, configuration):
        self.configuration = configuration
    
    def run(self, action_profile, action_map, actions, global_cooldown, player_state):
        pass

# configuration: A dict of the config.json file in the root directory.
# root: The base tkinter frame that this class's widget will be attached to.
class TrackerToolUI:
    def __init__(self, configuration, root):
        self.configuration = configuration
        self.on_display = []
        self.buffer = []
        self.widget = None
        
    def add_item(self, item):
        self.buffer.append(item)

    def get_widget(self):
        return self.widget

    @property
    def shape(self):
        pass

class TrackerToolConfiguration:
    def __init__(self, configuration):
        self.configuration = configuration

    def set_default_configuration(self):
        pass
    


        



