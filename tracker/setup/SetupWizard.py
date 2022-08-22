import pyautogui
import tkinter
from PIL import Image, ImageDraw, ImageTk
import json
import time
from tracker.util.Configurator import save_configuration_options
from tracker.setup.SetupWizardState import SetupWizardState
from tracker.setup.pages.WizardWelcomePage import WizardWelcomePage
from tracker.setup.pages.WizardAcknowledgePage import WizardAcknowledgePage
from tracker.setup.pages.WizardActionBarPresetSetupPage import WizardActionBarPresetSetupPage
from tracker.setup.pages.WizardActionBarSetupPage import WizardActionBarSetupPage

class SetupWizard:
    def __init__(self, configuration):
        self._configuration = configuration
        self._state = SetupWizardState.WELCOME_PAGE
        self._state = SetupWizardState.ACTION_BAR_PRESET_SETUP_PAGE
        self._root = tkinter.Tk()
        self._root.geometry('100x100')
        self._root.iconphoto(False,
                             ImageTk.PhotoImage(file=configuration['application-icon-file']))
        self._root.configure(highlightthickness=0)
        self._root.wm_attributes('-transparentcolor', self._configuration['setup-wizard-transparent-color'])
        self._root.title('LMT\'s Ability Tracker Setup Wizard')
        self._data = {'darkmode':True}

        self.load_state(self._state)

    def set_window_size(self, width, height):
        self._root.geometry('{}x{}'.format(width, height))

    def set_fullscreen(self, state):
        self._root.attributes('-fullscreen', state)

    def load_state(self, state):
        for prev_page in self._root.winfo_children():
            prev_page.destroy()

        self._state = state
        print('state:', state)
        page_constructor = None
        if state == SetupWizardState.WELCOME_PAGE:
            page_constructor = WizardWelcomePage
        elif state == SetupWizardState.ACKNOWLEDGE_PAGE:
            page_constructor = WizardAcknowledgePage
        elif state == SetupWizardState.ACTION_BAR_PRESET_SETUP_PAGE:
            page_constructor = WizardActionBarPresetSetupPage
        elif state == SetupWizardState.ACTION_BAR_SETUP_PAGE:
            page_constructor = WizardActionBarSetupPage
        elif state == SetupWizardState.KEYBIND_SETUP_PAGE:
            page_constructor = WizardActionBarKeybindSetupPage
        page = page_constructor(self._configuration, self.load_state,
                               self.add_data, self.get_data,
                               self.set_window_size, self.set_fullscreen,
                                self._root)
        widget = page.get_widget()
        widget.pack(fill=tkinter.BOTH)

    def add_data(self, key, value):
        self._data[key] = value

    def get_data(self, key):
        try:
            return self._data[key]
        except:
            return None

    def run(self):
        self._root.mainloop()

def run_setup_wizard(configuration):
    setup_wizard = SetupWizard(configuration)
    setup_wizard.run()
