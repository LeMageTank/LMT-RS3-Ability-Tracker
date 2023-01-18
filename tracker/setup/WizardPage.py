import tkinter
from PIL import Image, ImageDraw, ImageTk


class WizardPage:
    def __init__(self, configuration, load_page_fp,
                 add_data_fp, get_data_fp, set_window_size_fp,
                 set_fullscreen_fp, set_color_to_alpha_fp,
                 exit_setup_fp, parent_widget):
        self._configuration = configuration
        self._load_page_fp = load_page_fp
        self._add_data_fp = add_data_fp
        self._get_data_fp = get_data_fp
        self._set_window_size_fp = set_window_size_fp
        self._set_fullscreen_fp = set_fullscreen_fp
        self._set_color_to_alpha_fp = set_color_to_alpha_fp
        self._exit_setup_fp = exit_setup_fp
        self._widget = tkinter.Frame(parent_widget)

    def get_widget(self):
        pass
