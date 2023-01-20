from tracker.actions.ActionBar import ActionBar
from tracker.util.Configurator import Configurator
import json

class ActionBarController:
    def __init__(self, configuration):
        self.configuration = configuration
        self.weapon_switch_loadouts = {}
        self.load_input_profile()

    def load_input_profile(self):
        self._input_profile = None
        try:
            with open(self.configuration['input-profile'], 'r+') as file:
                self._input_profile = json.loads("".join(file.readlines()))
            if self._input_profile is None:
                raise Exception('Could not load input profile.')
            for key in ['action-bar-presets', 'action-bar-metadata', 'action-bars', 'weapon-switches', 'default-loadout']:
                if key not in self._input_profile.keys():
                    raise Exception('Missing field in input profile: ' + key)
        except Exception as e:
            Configurator.save_configuration_options({'user-has-completed-setup': False})
            with open(self.configuration['input-profile'], 'w+') as file:
                file.write('{}')
            raise e
        
        self.current_loaded_keybinds = []
        self.current_loaded_mousebinds = []

        self.load_action_bars()
        self.load_weapon_switch_loadouts()
        self.load_action_bar_presets()
        self.load_default_profile()

    def load_action_bars(self):
        self.action_bars = {}
        for action_bar_name, slots in self._input_profile['action-bars'].items():
            self.action_bars[action_bar_name] = ActionBar(action_bar_name, slots)

    def load_weapon_switch_loadouts(self):
        self.weapon_switch_loadouts = self._input_profile['weapon-switches']

    def load_action_bar_presets(self):
        self.action_bar_presets = []
        for action_bar_preset in self._input_profile['action-bar-presets']:
            self.action_bar_presets.append(action_bar_preset['slots'])

    def load_default_profile(self):
        for action_bar, preset_number in self._input_profile['default-loadout'].items():
            self.action_bars[action_bar].load_preset(self.action_bar_presets[preset_number])
        self.compile_bindings()

    def change_weapon(self, weapon_class):
        if weapon_class not in self.weapon_switch_loadouts.keys():
            return
        for action_bar, preset_number in self.weapon_switch_loadouts[weapon_class].items():
            if preset_number != -1:
                self.action_bars[action_bar].load_preset(self.action_bar_presets[preset_number])
        self.compile_bindings()

    def compile_bindings(self):
        self.current_loaded_keybinds = {}
        self.current_loaded_mousebinds = []
        for action_bar in self.action_bars.values():
            self.current_loaded_mousebinds.extend(action_bar.mousebinds)
            for keybind in action_bar.keybinds:
                self.current_loaded_keybinds[keybind.__hash__()] = keybind
        self.current_loaded_mousebinds.sort()

    def search_keybind(self, key):
        key = key[0].casefold() if key[1] is None else ''.join(key).casefold()
        try:
            return self.current_loaded_keybinds[key.__hash__()].actions
        except KeyError:
            return None

    def search_mousebind(self, key):
        first_index = 0
        last_index = len(self.current_loaded_mousebinds) - 1
        index = -1
        while first_index <= last_index and index == -1:
            middle_index = (first_index + last_index)//2
            if self.current_loaded_mousebinds[middle_index] == key:
                return self.current_loaded_mousebinds[middle_index].actions
            elif self.current_loaded_mousebinds[middle_index] < key:
                first_index = middle_index + 1
            else:
                last_index = middle_index - 1
        return None

    
