from pynput import mouse, keyboard
import multiprocessing
import subprocess
import pyautogui
import os
import json
import math
import time
from tracker.actions.Action import Action
from tracker.actions.KeybindAction import KeybindAction
from tracker.actions.ActionProfile import ActionProfile
from tracker.profilecreator import run_profilecreator
import importlib

class ActionTrackerController:
    global_cooldown = 1.8
    tick = 0.6
    def __init__(self, input_queue, controller_queue, configuration):
        self._configuration = configuration
        self._modifier_key = None
        self._control_queue = input_queue
        self._manager_queue = controller_queue
        self._profilecreator_process = None
        self.load_tracker()

        keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        keyboard_listener.start()
        
        mouse_listener = mouse.Listener(on_click=self.on_click)
        mouse_listener.start()

        self._action_queue = []
        self._last_action = 0

        self._tracker_tools = self.load_tools()

        self.paused = False

    def logfile(self, text):
        pass

    def mainloop(self):
        self.logfile('mainloop\n')
        while True:
            while self._control_queue.qsize() > 0:
                control_task = self._control_queue.get()
                if control_task == 'refresh':
                    self.load_tracker()
                elif control_task == 'pause':
                    self.paused = True
                    self._action_queue = []
                elif control_task == 'play':
                    self.paused = False
                elif control_task == 'configuration-open':
                    self.open_profilecreator()
                elif control_task == 'exit':
                    return
            if self.paused:
                time.sleep(self.tick)
                continue
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
                        self.update_weapon_profile(weapon=action.id)
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
                try:
                    for output in tool.run(self.action_profile, self._action_map, output_actions,
                                           min(activation_time - self._last_action, self.global_cooldown),
                                           player_state):
                        self._manager_queue.put(output)
                except Exception as e:
                    print("Error in tool: {}".format(tool.__class__.__name__))
                    print(e)

    def open_profilecreator(self):
        if self._profilecreator_process is not None and self._profilecreator_process.is_alive():
            return
        self._profilecreator_process = multiprocessing.Process(target=run_profilecreator, args=(self._configuration,))
        self._profilecreator_process.start()

    def load_tracker(self):
        self._weapon_map = self.load_weapons(self._configuration['weapons-file'])
        self._action_map = self.load_actions(self._configuration['action-info-file'])
        self._input_profiles = self.load_input_profiles(self._configuration['saved-profiles-metadata-file'],
                                                        self._configuration['saved-profiles-directory'])
        self.update_weapon_profile(profile=self._configuration['default-profile'])

    def load_tools(self):
        self.logfile('load_tools\n')
        tools = []
        for tool in self._configuration['tools']:
            if tool['enabled'] is False:
                continue
            self.logfile('\t{}\n'.format(tool['file-name']))
            spec = importlib.util.spec_from_file_location(tool['file-name'], self._configuration['tools-path'] + tool['file-name'] + '.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            tool_class = getattr(module, tool['tracker-tool'])
            tools.append(tool_class(self._configuration))
        return tools
            
    def update_weapon_profile(self, profile=None, weapon=None):
        self.logfile('update_weapon_profile\n')
        if weapon:
            self.action_profile = self._input_profiles[self._weapon_map[weapon]]
            self.action_profile.weapon = weapon
        if profile:
            self.action_profile = self._input_profiles[profile]

    def load_weapons(self, weapons_path):
        self.logfile('load_weapons\n')
        with open(weapons_path, 'r+') as file:
            loaded_weapons = json.loads("".join(file.readlines()))
            weapon_map = {}
            for weapon_class in loaded_weapons['weapon_profiles']:
                for weapon in weapon_class['weapons']:
                    weapon_map[weapon] = weapon_class['weapon_type']
            return weapon_map
                  
    def load_actions(self, actioninfo_path):
        self.logfile('load_actions\n')
        with open(actioninfo_path, 'r+') as file:
            loaded_actions = json.loads("".join(file.readlines()))
            action_map = {}
            for action in loaded_actions:
                action_map[action['action']] = Action(action)
            return action_map
        
    def load_input_profiles(self, profiles_metadata_path, saved_profiles_directory):
        self.logfile('load_input_profiles\n')
        with open(profiles_metadata_path, 'r+') as profiles_metadata_file:
            profiles_metadata = json.loads("".join(profiles_metadata_file.readlines()))
            input_profiles = {}
            for profile in profiles_metadata['profiles']:
                with open(saved_profiles_directory + profile['save_file'], 'r+') as profile_file:
                    profile_data = json.loads("".join(profile_file.readlines()))
                    input_profiles[profile['activator_weapons']] = ActionProfile(profile_data, profile['activator_weapons'])
            return input_profiles

    def get_player_state(self):
        self.logfile('get_player_state\n')
        player_state = {}
        if self.action_profile.adrenaline_bar is not None:
            adrenaline_bar = pyautogui.screenshot(region=self.action_profile.adrenaline_bar)
            pixel_reader = adrenaline_bar.load()
            adrenaline_pixels = 0
            for i in range(adrenaline_bar.size[0]):
                r,g,b = pixel_reader[i,0]
                if r > 180 and g > 90:
                    adrenaline_pixels += 1
            adrenaline = math.ceil((adrenaline_pixels)*100/(self.action_profile.adrenaline_bar[2] - 1))
            player_state['adrenaline'] = adrenaline
        else:
            player_state['adrenaline'] = None
        return player_state

    def on_click(self, x, y , button, pressed):
        if self.paused:
            return
        if pressed:
            action = self.action_profile.search_mousebind((x,y))
            if action:
                self._action_queue.append(action)

    def on_press(self, key):
        if self.paused:
            return
        if key in KeybindAction.modifier_keys:
            self._modifier_key = key
        else:
            try:
                key = chr(key.vk)
                if key in KeybindAction.special_key_map.keys():
                    key = KeybindAction.special_key_map[key]
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

# manager_queue: manager -> UI
# control_queue: UI/User -> manager
def run_tracker_controller(input_queue, controller_queue, configuration):
    tracker = ActionTrackerController(input_queue, controller_queue, configuration)
    tracker.mainloop()
