from ahk import AHK
from pynput import mouse, keyboard
import pyautogui
import multiprocessing
import os
import json
import time
import tkinter
from PIL import Image, ImageDraw, ImageTk
import numpy as np
from ability import *


class AbilityTracker:
    def __init__(self, ui_queue, default_profile):
        self._ahk = AHK(executable_path='app\\ahk\\AutoHotkey.exe')
        self._ui_queue = ui_queue
        self._input_queue = []
        self._mouse_abilties = []
        self._mouse_abilities = []
        self._modifier_key = None

        self._weapon_map = self.load_weapons('app\\data\\weapons.json')
        self._ability_map = self.load_abilities('app\\data\\abilityinfo.json')
        self._input_profiles = self.load_input_profiles('app\\data\\saved_profiles.json', 'app\\data\\saved profiles\\')
        self.update_weapon_profile(default_profile)

        keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        keyboard_listener.start()
        
        mouse_listener = mouse.Listener(on_click=self.on_click)
        mouse_listener.start()

        self._ability_queue = []
        self._last_ability = 0
    
    def mainloop(self):
        ability_queue_buffer = []
        ability_buffer = []
        while(True):
            output_queue = []
            activation_time = time.time()
            while(len(self._ability_queue) > 0):
                activator = self._ability_queue.pop(0)
                try:
                    ability = self._ability_map[activator._name]
                    if(ability.ability_type == 'weapon'):
                        self.update_weapon_profile(self._weapon_map[ability.name])
                        output_queue.append(ability.name)
                    elif(ability.incurs_gcd):
                        ability_buffer.append(ability)
                    else:
                        if(ability.activate(activation_time)):
                            output_queue.append(ability.name)
                except:
                    output_queue.append(activator._name)
            if(activation_time - self._last_ability >= 0.6):
                while(len(ability_buffer) > 0):
                    ability = ability_buffer.pop(-1)
                    if(ability.activate(activation_time)):
                        self._last_ability = activation_time
                        self._ui_queue.put(ability.name)
                        ability_buffer = []
                        ability_queue_buffer = []
                        break
                    else:
                        ability_queue_buffer.append(ability)
                ability_buffer = ability_queue_buffer
                ability_queue_buffer = []
            else:
                if(len(ability_buffer) > 0):
                    ability_buffer = [ability_buffer[-1]]
            time.sleep(0.1)
            if(len(output_queue) > 0):
                for abil in output_queue:
                    self._ui_queue.put(abil)
                output_queue = []

    def update_weapon_profile(self, profile_name):
        self._clicked_abilities = self._input_profiles[profile_name]['mouse_ability_tree'] 
        self._pressed_abilities = self._input_profiles[profile_name]['keypress_ability_tree']

    def load_weapons(self, path):
        f = open(path, 'r+')
        loaded_weapons = json.loads("".join(f.readlines()))
        f.close()
        weapon_map = {}
        for weapon_class in loaded_weapons['weapon_profiles']:
            for weapon in weapon_class['weapons']:
                weapon_map[weapon] = weapon_class['weapon_type']
        return weapon_map
                  
    def load_abilities(self, path):
        f = open(path, 'r+')
        loaded_abilities = json.loads("".join(f.readlines()))
        ability_map = {}
        f.close()
        for ability in loaded_abilities:
            ability_map[ability['ability']] = Ability(ability)
        return ability_map
        
    def load_input_profiles(self, profiles_metadata_path, saved_profiles_directory):
        f = open(profiles_metadata_path, 'r+')
        profiles_metadata = json.loads("".join(f.readlines()))
        f.close()
        input_profiles = {}
        for profile in profiles_metadata['profiles']:
            f = open(saved_profiles_directory + profile['save_file'])
            profile_data = json.loads("".join(f.readlines()))
            f.close()
            for i in range(len(profile_data['keypress_activated'])):
                profile_data['keypress_activated'][i] = KeypressAbility(profile_data['keypress_activated'][i])
            for i in range(len(profile_data['mouse_activated'])):
                profile_data['mouse_activated'][i] = ClickableAbility(profile_data['mouse_activated'][i])
            profile_data['keypress_ability_tree'] = AbilitySearchTree(profile_data['keypress_activated'])
            profile_data['mouse_ability_tree'] = AbilitySearchTree(profile_data['mouse_activated'])
            input_profiles[profile['activator_weapons']] = profile_data
        return input_profiles

    def on_click(self, x, y , button, pressed):
        if(pressed):
            abil = self._clicked_abilities.search((x,y))
            if(abil):
                self._ability_queue.append(abil)

    def on_press(self, key):
        if(key in KeypressAbility.modifier_keys):
            self._modifier_key = key
        else:
            abil = None
            try:
                if(self._modifier_key is None):
                    abil = self._pressed_abilities.search((chr(key.vk).lower(), None))
                else:
                    abil = self._pressed_abilities.search((chr(key.vk).lower(), self._modifier_key.name))
            except:
                if(self._modifier_key is None):
                    abil = self._pressed_abilities.search((str(key), None))
                else:
                    abil = self._pressed_abilities.search((str(key), self._modifier_key.name))
            if(abil):
                self._ability_queue.append(abil)
            
    def on_release(self, key):
        if(key == self._modifier_key):
            self._modifier_key = None

class AbilityTrackerUI:
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
        self._root.iconphoto(False,ImageTk.PhotoImage(file='app\\data\\app icons\\icon.png'))
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
        for i in range(len(self._ability_queue)):
            try:
                image_widget = tkinter.Label(self._root, image=self._icon_map[self._ability_queue[i]], background='black')
                image_widget.pack(side='right', fill='none', pady=self._padding[1], padx=self._padding[0])
            except:
                image_widget = tkinter.Label(self._root, text="?", background='black')
                image_widget.pack(side='right', fill='none', pady=self._padding[1], padx=self._padding[0])
        self._root.after(self._update_interval, self.update)


def run_tracker(ui_queue):
    tracker = AbilityTracker(ui_queue, '2h_melee')
    tracker.mainloop()
 
