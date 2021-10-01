from pynput import mouse, keyboard
import multiprocessing
import os
import json
import math
import time
import tkinter
import pyautogui
from PIL import Image, ImageDraw, ImageTk
import numpy as np
from action import Action, KeybindAction, ActionProfile
import importlib


class TrackerManager:
    global_cooldown = 1.8
    tick = 0.6
    def __init__(self, manager_queue, configuration):
        self._configuration = configuration
        self._manager_queue = manager_queue
        self._modifier_key = None

        self._weapon_map = self.load_weapons(configuration['weapons-file'])
        self._action_map = self.load_actions(configuration['action-info-file'])
        self._input_profiles = self.load_input_profiles(configuration['saved-profiles-metadata-file'],
                                                        configuration['saved-profiles-directory'])
        self.update_weapon_profile(configuration['default-profile'])

        keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        keyboard_listener.start()
        
        mouse_listener = mouse.Listener(on_click=self.on_click)
        mouse_listener.start()

        self._action_queue = []
        self._last_action = 0

        self._tracker_tools = self.load_tools()

    def mainloop(self):
        while True:
            time.sleep(self.tick)
            queued_action = None
            output_actions = []
            activation_time = time.time()
            gcd_incurred = (activation_time - self._last_action) < self.global_cooldown
            # Pop off the oldest action until the queue is empty
            while len(self._action_queue) > 0:
                bound_action = self._action_queue.pop(0)
                try:
                    action = self._action_map[bound_action.action]
                    # Weapon swap, change input profile
                    if action.action_type == 'weapon':
                        self.update_weapon_profile(self._weapon_map[action.id])
                        output_actions.append(action.id)
                    # Action incurs the global cooldown
                    elif action.incurs_gcd:
                        # If action is off cooldown and the last gcd is over, activate it
                        if action.can_activate(activation_time) and not gcd_incurred:
                            action.activate(activation_time)
                            output_actions.append(action.id)
                            self._last_action = activation_time
                            gcd_incurred = True
                        # The action is on cooldown or the gcd is active, queue the action
                        else:
                            queued_action = bound_action
                    # The action does not incur the gcd, can be used if off cooldown
                    else:
                        if action.activate(activation_time):
                            output_actions.append(action.id)
                # The action is not a registered ability/weapon/item,
                # it's name will be passed on.
                except KeyError:
                    output_actions.append(bound_action.action)
            if queued_action:
                self._action_queue.insert(0, queued_action)
            player_state = self.get_player_state()
            for tool in self._tracker_tools:
                for output in tool.run(self.action_profile, self._action_map, output_actions,
                                       min(activation_time - self._last_action, self.global_cooldown),
                                       player_state):
                    self._manager_queue.put(output)

    def load_tools(self):
        tools = []
        for tool in self._configuration['tools']:
            if tool['enabled'] is False:
                continue
            spec = importlib.util.spec_from_file_location(tool['file-name'], self._configuration['tools-path'] + tool['file-name'] + '.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            tool_class = getattr(module, tool['tracker-tool'])
            tools.append(tool_class(self._configuration))
        return tools
            
    def update_weapon_profile(self, profile_name):
        self.action_profile = self._input_profiles[profile_name]

    def load_weapons(self, weapons_path):
        with open(weapons_path, 'r+') as file:
            loaded_weapons = json.loads("".join(file.readlines()))
            weapon_map = {}
            for weapon_class in loaded_weapons['weapon_profiles']:
                for weapon in weapon_class['weapons']:
                    weapon_map[weapon] = weapon_class['weapon_type']
            return weapon_map
                  
    def load_actions(self, actioninfo_path):
        with open(actioninfo_path, 'r+') as file:
            loaded_actions = json.loads("".join(file.readlines()))
            action_map = {}
            for action in loaded_actions:
                action_map[action['action']] = Action(action)
            return action_map
        
    def load_input_profiles(self, profiles_metadata_path, saved_profiles_directory):
        with open(profiles_metadata_path, 'r+') as profiles_metadata_file:
            profiles_metadata = json.loads("".join(profiles_metadata_file.readlines()))
            input_profiles = {}
            for profile in profiles_metadata['profiles']:
                with open(saved_profiles_directory + profile['save_file'], 'r+') as profile_file:
                    profile_data = json.loads("".join(profile_file.readlines()))
                    input_profiles[profile['activator_weapons']] = ActionProfile(profile_data, profile['activator_weapons'])
            return input_profiles

    def get_player_state(self):
        adrenaline_bar = pyautogui.screenshot(region=self.action_profile.adrenaline_bar)
        pixel_reader = adrenaline_bar.load()
        adrenaline_pixels = 0
        for i in range(adrenaline_bar.size[0]):
            r,g,b = pixel_reader[i,0]
            if r > 180 and g > 90:
                adrenaline_pixels += 1
        adrenaline = math.ceil((adrenaline_pixels)*100/(self.action_profile.adrenaline_bar[2] - 1))
        player_state = {'adrenaline':adrenaline}
        return player_state

    def on_click(self, x, y , button, pressed):
        if pressed:
            action = self.action_profile.search_mousebind((x,y))
            if action:
                self._action_queue.append(action)

    def on_press(self, key):
        if key in KeybindAction.modifier_keys:
            self._modifier_key = key
        else:
            try:
                key = chr(key.vk)
            except AttributeError:
                try:
                    key = KeybindAction.special_key_map[str(key).casefold()]
                except KeyError:
                    return
            action = self.action_profile.search_keybind((key, None if self._modifier_key is None else KeybindAction.modifier_key_map[self._modifier_key.name]))
            if action:
                self._action_queue.append(action)

            
    def on_release(self, key):
        if key == self._modifier_key:
            self._modifier_key = None

class TrackerUI:
    def __init__(self, configuration, tracker_queue):
        self._configuration = configuration
        self._root = tkinter.Tk()
        self._icon_map = self.load_icons(configuration['action-icon-directory'])
        self._icon_history = []
        self._max_icons = configuration['actiontracker-icons']
        self._update_interval = configuration['actiontracker-update-interval']
        self._icon_shape = configuration['actiontracker-icon-shape']
        self._padding = configuration['actiontracker-icon-padding']
        self._tracker_queue = tracker_queue
        self._ability_queue = []
        self._root.title("LMT's Ability Tracker")
        self._root.attributes('-topmost', configuration['actiontracker-always-on-top'])
        self._root.iconphoto(False,ImageTk.PhotoImage(file=configuration['application-icon-file']))
        
        self._root.bind('<B1-Motion>', self.move_window)
        self._root.configure(background='black')

        self._uitracker_tools = self.load_tools()
        self._root.geometry("{}x{}".format(self._tool_width, self._tool_height))

    def move_window(self, event):
        x,y = self._root.winfo_pointerxy()
        self._root.geometry("{}x{}+{}+{}".format(self._tool_width, self._tool_height, x, y))

    def load_tools(self):
        num_tools = 0
        self._tool_width = 0
        self._tool_height = 10
        tools = {}
        for tool in self._configuration['tools']:
            if tool['enabled'] is False:
                continue
            spec = importlib.util.spec_from_file_location(tool['file-name'], self._configuration['tools-path'] + tool['file-name'] + '.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            tool_class = getattr(module, tool['tracker-tool-ui'])
            tool_ui = tool_class(self._configuration, self._root)
            self._tool_width = max(self._tool_width, tool_ui.shape[0])
            self._tool_height += tool_ui.shape[1]
            tool_widget = tool_ui.get_widget().grid(row=num_tools, sticky=tkinter.W)
            num_tools += 1
            tools[tool['name']] = tool_ui
        return tools

    def load_icons(self, path):
        icon_map = {}
        for file in os.listdir(path):
            icon = tkinter.PhotoImage(file=(path + file))
            icon_map[file.split('.')[0]] = icon
        return icon_map

    def run(self):
        self.update()
        self._root.mainloop()

    def update(self):
        while self._tracker_queue.qsize() > 0:
            item = self._tracker_queue.get()
            self._uitracker_tools[item[0]].add_item(item[1])

        for name, tool in self._uitracker_tools.items():
            tool.draw(self._icon_map)
            
        self._root.after(self._update_interval, self.update)


def run_tracker(manager_queue, configuration):
    tracker = TrackerManager(manager_queue, configuration)
    tracker.mainloop()
 
