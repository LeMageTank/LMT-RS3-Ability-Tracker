import pyautogui
import tkinter
from PIL import Image, ImageDraw, ImageTk
import json
import time
from tracker.util.Configurator import Configurator
from tracker.actions.KeybindAction import KeybindAction
from tracker.actions.MousebindAction import MousebindAction
from tracker.setup.SetupWizardPageProvider import SetupWizardPageProvider
from tracker.setup.SetupWizardPageState import SetupWizardPageState
from tracker.util.InputProfileJsonEncoder import InputProfileJsonEncoder


class SetupWizard:
    def __init__(self, configuration):
        self._configuration = configuration
        self._root = tkinter.Tk()
        self._root.geometry('100x100')
        self._root.iconphoto(False,
                             ImageTk.PhotoImage(file=configuration['application-icon-file']))
        self._root.configure(highlightthickness=0)
        self._root.wm_attributes('-transparentcolor', self._configuration['setup-wizard-transparent-color'])
        self._root.title('LMT\'s Ability Tracker Setup Wizard')
        self._data = {'darkmode':True}
        self.load_input_profile()
        self._page = None
        self.load_page(SetupWizardPageState.WELCOME_PAGE)

    def set_window_size(self, width, height):
        self._root.geometry('{}x{}'.format(width, height))

    def set_fullscreen(self, state):
        self._root.attributes('-fullscreen', state)

    def set_color_to_alpha(self, color):
        self._root.wm_attributes("-transparentcolor", color)

    def load_page(self, page_state):
        print('Loading page:', page_state)
        page_constructor = SetupWizardPageProvider.get_page_constructor(page_state)
        for prev_page in self._root.winfo_children():
            prev_page.destroy()

        self._page = page_constructor(self._configuration, self.load_page,
                               self.add_data, self.get_data,
                               self.set_window_size, self.set_fullscreen,
                               self.set_color_to_alpha, self.exit, self._root)
        widget = self._page.get_widget()
        widget.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        self.set_color_to_alpha('#00D500')

    def add_data(self, key, value):
        self._data[key] = value

    def get_data(self, key):
        try:
            return self._data[key]
        except:
            return None

    def load_input_profile(self):
        input_profile = None
        with open(self._configuration['input-profile'], 'r+') as file:
            input_profile = json.loads("".join(file.readlines()))
        for key, value in input_profile.items():
            self.add_data(key, value)

    def save_input_profile(self):
        del self._data['darkmode']
        with open(self._configuration['input-profile'], 'w') as file:
            file.write(json.dumps(self._data, indent=4, cls=InputProfileJsonEncoder))

    def run(self):
        self._root.mainloop()

    def exit(self, save):
        if save:
            self.save_input_profile()
            Configurator.save_configuration_options({'user-has-completed-setup': True})
        self._root.destroy()


def run_setup_wizard(configuration):
    setup_wizard = SetupWizard(configuration)
    setup_wizard.run()
