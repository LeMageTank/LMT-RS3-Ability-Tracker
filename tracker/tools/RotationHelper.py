from tracker.trackertools import TrackerTool, TrackerToolUI, TrackerToolConfiguration
import pyautogui
import math
import time
import tkinter
import itertools

class RotationHelper(TrackerTool):
    def __init__(self, configuration):
        super().__init__(configuration)
        if configuration['rotation-helper-rotation'] == 'dps':
            self.rotation = DPSRotation()
        elif configuration['rotation-helper-rotation'] == 'berserk':
            self.rotation = BerserkRotation()

    def run(self, action_profile, action_map, actions, global_cooldown, player_state):
        output_list = []
        for action in self.rotation.run(action_profile, action_map, actions, player_state, global_cooldown):
            output_list.append(('rotation-helper', action))
        return output_list

class RotationHelperUI(TrackerToolUI):
    def __init__(self, configuration, root):
        super().__init__(configuration, root)
        self._shape = configuration['rotation-helper-icon-shape']
        self.padding = configuration['rotation-helper-icon-padding']
        self.widget = tkinter.Frame(root, background='black')

    def draw(self, icon_map):
        if len(self.buffer) == 0:
            return
        for child in self.widget.winfo_children():
            child.destroy()
        for action in self.buffer:
            try:
                action_widget = tkinter.Label(self.widget, image=icon_map[action], background='black')
                action_widget.pack(side='left', fill='none', pady=self.padding[1], padx=self.padding[0])
            except:
                action_widget = tkinter.Label(self.widget, text="Missing", background='black')
                action_widget.pack(side='left', fill='none', pady=self.padding[1], padx=self.padding[0])
        self.buffer = []

    @property
    def shape(self):
        return tuple(self._shape)

class BerserkRotation:
    def __init__(self):
        self.th_basics_order_berserk = ['Cleave', 'Sever', 'Fury', 'Smash',
                                'Slice', 'Sacrifice', 'Kick', 'Backhand', 'Punish']
        self.th_basics_order = ['Dismember', 'Cleave', 'Sever', 'Fury', 'Smash',
                                'Slice', 'Sacrifice', 'Kick', 'Backhand', 'Punish']
        self.th_thresholds_order = ['Assault', 'Hurricane', 'Blood Tendrils', 'Quake', 'Forceful Backhand', 'Slaughter']
        self.th_thresholds_order_berserk = ['Assault', 'Hurricane', 'Quake', 'Forceful Backhand']
        self.dw_basics_order = ['Dismember', 'Decimate', 'Sever', 'Fury', 'Havoc',
                                'Slice', 'Sacrifice', 'Kick', 'Backhand', 'Punish']
        self.dw_thresholds_order = ['Assault', 'Destroy', 'Blood Tendrils', 'Forceful Backhand', 'Flurry', 'Slaughter']

    def run(self, action_profile, action_map, actions, player_state, global_cooldown):
        current_time = time.time()

        # Estimate the adrenaline the player will have by the end of the gcd after their most recent ability
        forward_adrenaline_delta = 0
        for action in actions:
            try:
                forward_adrenaline_delta += action_map[action].adrenaline_delta
            except:
                pass
        if action_profile.weapon_type == '2h_melee':
            if action_map['Berserk'].can_activate(current_time + global_cooldown):
                if player_state['adrenaline'] + forward_adrenaline_delta >= 100:
                    return ['Enhanced Replenishment Potion', 'Ring of Vigour', 'Berserk']
                else:
                    for basic in self.th_basics_order:
                        if action_map[basic].can_activate(current_time + global_cooldown):
                            return [basic]
            elif action_map['Berserk'].cooldown_remaining(current_time + global_cooldown) >= 40:
                if player_state['adrenaline'] + forward_adrenaline_delta >= 50:
                    for threshold in self.th_thresholds_order_berserk:
                        if action_map[threshold].can_activate(current_time + global_cooldown):
                            return [threshold]
                for basic in self.th_basics_order_berserk:
                    if action_map[basic].can_activate(current_time + global_cooldown):
                        return [basic]
            elif action_map['Berserk'].cooldown_remaining(current_time + global_cooldown) > 20:
                if player_state['adrenaline'] + forward_adrenaline_delta >= 50:
                    for threshold in self.th_thresholds_order:
                        if action_map[threshold].can_activate(current_time + global_cooldown):
                            return [threshold]
            for basic in self.th_basics_order:
                if action_map[basic].can_activate(current_time + global_cooldown):
                    return [basic]
        elif action_profile.weapon_type == 'dw_melee':
            if action_map['Berserk'].can_activate(current_time + global_cooldown):
                if player_state['adrenaline'] + forward_adrenaline_delta >= 100:
                    return ['Enhanced Replenishment Potion', 'Ring of Vigour', 'Berserk']
                else:
                    for basic in self.dw_basics_order:
                        if action_map[basic].can_activate(current_time + global_cooldown):
                            return [basic]
            elif action_map['Berserk'].cooldown_remaining(current_time + global_cooldown) > 20:
                if player_state['adrenaline'] + forward_adrenaline_delta >= 50:
                    for threshold in self.dw_thresholds_order:
                        if action_map[threshold].can_activate(current_time + global_cooldown):
                            return [threshold]
            elif action_map['Berserk'].cooldown_remaining(current_time + global_cooldown) > 40:
                for threshold in self.dw_thresholds_order:
                    if action_map[threshold].can_activate(current_time + global_cooldown):
                        return [threshold]
                for basic in self.dw_basics_order[1::]:
                    if action_map[basic].can_activate(current_time + global_cooldown):
                        return [basic]
            for basic in self.dw_basics_order:
                if action_map[basic].can_activate(current_time + global_cooldown):
                    return [basic]
        return []

class DPSRotation:
    def __init__(self):
        self.th_basics_order = ['Dismember', 'Cleave', 'Sever', 'Fury', 'Smash',
                       'Slice', 'Sacrifice', 'Kick', 'Backhand', 'Punish']
        self.th_thresholds_order = ['Assault', 'Hurricane', 'Blood Tendrils', 'Quake', 'Forceful Backhand', 'Slaughter']
        self.dw_basics_order = ['Dismember', 'Decimate', 'Sever', 'Fury', 'Havoc', 'Slice']
        self.dw_thresholds_order = ['Assault', 'Destroy', 'Blood Tendrils', 'Forceful Backhand', 'Flurry', 'Slaughter']
    
    def run(self, action_profile, action_map, actions, player_state, global_cooldown):
        current_time = time.time()

        # Estimate the adrenaline the player will have by the end of the gcd after their most recent ability
        forward_adrenaline_delta = 0
        for action in actions:
            try:
                forward_adrenaline_delta += action_map[action].adrenaline_delta
            except:
                pass

        if action_profile.weapon_type == '2h_melee':
            if player_state['adrenaline'] + forward_adrenaline_delta > 50:
                for threshold in self.th_thresholds_order:
                    if action_map[threshold].can_activate(current_time + global_cooldown):
                        return [threshold]
            for basic in self.th_basic_order:
                if action_map[basic].can_activate(current_time + global_cooldown):
                    return [basic]
        elif action_profile.weapon_type == 'dw_melee':
            if player_state['adrenaline'] + forward_adrenaline_delta > 50:
                for threshold in self.dw_thresholds_order:
                    if action_map[threshold].can_activate(current_time + global_cooldown):
                        return [threshold]
            for basic in self.dw_basics_order:
                if action_map[basic].can_activate(current_time + global_cooldown):
                    return [basic]
        # No available abilities off cooldown or the player is using another weapon style
        return []

class RotationHelperConfiguration(TrackerToolConfiguration):
    def set_default_configuration(self):
        self.configuration['rotation-helper-rotation'] = 'dps'
        self.configuration['rotation-helper-icon-shape'] = [30,30]
        self.configuration['rotation-helper-icon-padding'] = [4,4]
