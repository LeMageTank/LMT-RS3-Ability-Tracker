import tkinter
from PIL import Image, ImageDraw, ImageTk
from tracker.setup.SetupWizardState import SetupWizardState


class WizardWidget:
    def __init__(self, configuration, load_state_fp,
                 add_data_fp, get_data_fp, set_window_size_fp,
                 set_fullscreen_fp, parent_widget):
        self._configuration = configuration
        self._load_state_fp = load_state_fp
        self._add_data_fp = add_data_fp
        self._get_data_fp = get_data_fp
        self._set_window_size_fp = set_window_size_fp
        self._set_fullscreen_fp = set_fullscreen_fp
        self._widget = tkinter.Frame(parent_widget)

    def get_widget(self):
        pass
