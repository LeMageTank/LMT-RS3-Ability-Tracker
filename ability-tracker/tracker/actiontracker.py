from pynput import mouse, keyboard
import multiprocessing
import os
import json
import time
import tkinter
from PIL import Image, ImageDraw, ImageTk
import numpy as np
from action import Action, KeybindAction, ActionProfile


class ActionTracker:
    global_cooldown = 1.8
    tick = 0.6
    def __init__(self, ui_queue, default_profile):
        self._ui_queue = ui_queue
        self._modifier_key = None

        self._weapon_map = self.load_weapons('ability-tracker\\data\\weapons.json')
        self._action_map = self.load_actions('ability-tracker\\data\\abilityinfo.json')
        self._input_profiles = self.load_input_profiles('ability-tracker\\data\\saved_profiles.json', 'ability-tracker\\data\\saved profiles\\')
        self.update_weapon_profile(default_profile)

        keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        keyboard_listener.start()
        
        mouse_listener = mouse.Listener(on_click=self.on_click)
        mouse_listener.start()

        self._action_queue = []
        self._last_action = 0
        

    def mainloop(self):
        while True:
            time.sleep(self.tick)
            queued_action = None
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
                        self._ui_queue.put(action.id)
                    # Action incurs the global cooldown
                    elif action.incurs_gcd:
                        # If action is off cooldown and the last gcd is over, activate it
                        if action.can_activate(activation_time) and not gcd_incurred:
                            action.activate(activation_time)
                            self._ui_queue.put(action.id)
                            self._last_action = activation_time
                            gcd_incurred = True
                        # The action is on cooldown or the gcd is active, queue the action
                        else:
                            queued_action = bound_action
                    # The action does not incur the gcd, can be used if off cooldown
                    else:
                        if action.activate(activation_time):
                            self._ui_queue.put(action.id)
                # The action is not a registered ability/weapon/item,
                # it's name will be passed to the ui_queue. 
                except KeyError:
                    self._ui_queue.put(bound_action.action)
            if queued_action:
                self._action_queue.insert(0, queued_action)
                        

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
                action_map[action['ability']] = Action(action)
            return action_map
        
    def load_input_profiles(self, profiles_metadata_path, saved_profiles_directory):
        with open(profiles_metadata_path, 'r+') as profiles_metadata_file:
            profiles_metadata = json.loads("".join(profiles_metadata_file.readlines()))
            input_profiles = {}
            for profile in profiles_metadata['profiles']:
                with open(saved_profiles_directory + profile['save_file'], 'r+') as profile_file:
                    profile_data = json.loads("".join(profile_file.readlines()))
                    input_profiles[profile['activator_weapons']] = ActionProfile(profile_data)
            return input_profiles

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

class ActionTrackerUI:
    def __init__(self, icons_path, max_icons, update_interval, icon_shape, padding, tracker_queue):
        self._root = tkinter.Tk()
        self._icon_map = self.load_icons(icons_path)
        self._icon_history = []
        self._max_icons = max_icons
        self._update_interval = update_interval
        self._icon_shape = icon_shape
        self._padding = padding
        self._tracker_queue = tracker_queue
        self._ability_queue = []
        self._root.title("LMT's Ability Tracker")
        self._root.attributes('-topmost', True)
        self._root.iconphoto(False,ImageTk.PhotoImage(file='ability-tracker\\data\\app icons\\icon.png'))
        self._root.geometry("{}x{}".format(((self._icon_shape[0]+1) * self._padding[0]) +
                                           self._icon_shape[0]*self._max_icons,
                                           self._icon_shape[1] + (self._padding[1] * 2)))
        self._root.bind('<B1-Motion>', self.move_window)
        self._root.configure(background='black')

    def move_window(self, event):
        x,y = self._root.winfo_pointerxy()
        self._root.geometry("{}x{}+{}+{}".format(((self._icon_shape[0]+1) * self._padding[0]) +
                                           self._icon_shape[0]*self._max_icons,
                                           self._icon_shape[1] + (self._padding[1] * 2), x, y))

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
        while(self._tracker_queue.qsize() > 0):
            self._ability_queue.append(self._tracker_queue.get())
        for widget in self._root.winfo_children():
            widget.destroy()
        while(len(self._ability_queue) > self._max_icons):
            self._ability_queue.pop(0)
        for i in range(len(self._ability_queue)-1, -1, -1):
            try:
                image_widget = tkinter.Label(self._root, image=self._icon_map[self._ability_queue[i]], background='black')
                image_widget.pack(side='right', fill='none', pady=self._padding[1], padx=self._padding[0])
            except:
                image_widget = tkinter.Label(self._root, text="?", background='black')
                image_widget.pack(side='right', fill='none', pady=self._padding[1], padx=self._padding[0])
        self._root.after(self._update_interval, self.update)


def run_tracker(ui_queue):
    tracker = ActionTracker(ui_queue, '2h_melee')
    tracker.mainloop()
 
