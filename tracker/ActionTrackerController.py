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
from tracker.actions.ActionBarController import ActionBarController
from tracker.setup.SetupWizard import run_setup_wizard
import importlib

class ActionTrackerController:
    global_cooldown = 1.8
    tick = 0.6
    def __init__(self, input_queue, controller_queue, configuration):
        self._configuration = configuration
        self._modifier_key = None
        self._control_queue = input_queue
        self._manager_queue = controller_queue
        self.load_tracker()

        keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        keyboard_listener.start()
        
        mouse_listener = mouse.Listener(on_click=self.on_click)
        mouse_listener.start()

        self._action_queue = []
        self._last_action = 0

        self._tracker_tools = self.load_tools()

        self.paused = False

    def mainloop(self):
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
                    self.load_setup_wizard()
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
                action_id = self._action_queue.pop(0)
                try:
                    action = self._action_map[action_id]
                    # Weapon swap, change input profile
                    if action.action_type == 'weapon':
                        self.swap_weapons(action.id)
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
                            queued_action = action_id
                    # The action does not incur the gcd, can be used if off cooldown
                    else:
                        if action.activate(activation_time):
                            output_actions.append(action.id)
                # The action is not a registered ability/weapon/item,
                # it's name will be passed on.
                except KeyError:
                    output_actions.append(action_id)
            if queued_action:
                self._action_queue.insert(0, queued_action)
            player_state = self.get_player_state()
            for tool in self._tracker_tools:
                try:
                    for output in tool.run(self._action_map, output_actions,
                                           min(activation_time - self._last_action, self.global_cooldown),
                                           player_state):
                        self._manager_queue.put(output)
                except Exception as e:
                    print("Error in tool: {}".format(tool.__class__.__name__))
                    raise e

    def load_tracker(self):
        self.load_weapons()
        self.load_input_profile()
        self._action_map = self.load_actions(self._configuration['action-info-file'])

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

    def swap_weapons(self, weapon):
        if weapon not in self.weapon_map.keys():
            return
        weapon_class = self.weapon_map[weapon]
        self.action_bar_controller.change_weapon(weapon_class)

    def load_setup_wizard(self):
        run_setup_wizard(self._configuration)

    def load_weapons(self):
        self.weapon_map = {}
        with open(self._configuration['weapons-file'], 'r+') as file:
            weapons = json.loads("".join(file.readlines()))
            for weapon_set in weapons['weapon_profiles']:
                weapon_class = weapon_set['weapon_type']
                for weapon in weapon_set['weapons']:
                    self.weapon_map[weapon] = weapon_class
                  
    def load_actions(self, actioninfo_path):
        with open(actioninfo_path, 'r+') as file:
            loaded_actions = json.loads("".join(file.readlines()))
            action_map = {}
            for action in loaded_actions:
                action_map[action['action']] = Action(action)
            return action_map

    def load_input_profile(self):
        self.action_bar_controller = ActionBarController(self._configuration)

    def get_player_state(self):
        player_state = {'adrenaline': None}
        return player_state

    def on_click(self, x, y , button, pressed):
        if self.paused:
            return
        if pressed:
            actions = self.action_bar_controller.search_mousebind((x,y))
            if actions:
                self._action_queue.extend(actions)

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
            actions = self.action_bar_controller.search_keybind((key, None if self._modifier_key is None else KeybindAction.modifier_key_map[self._modifier_key.name]))
            if actions:
                self._action_queue.extend(actions)
            
    def on_release(self, key):
        if key == self._modifier_key:
            self._modifier_key = None

            
def run_tracker_controller(input_queue, controller_queue, configuration):
    print('Starting tracker')
    tracker = ActionTrackerController(input_queue, controller_queue, configuration)
    tracker.mainloop()
