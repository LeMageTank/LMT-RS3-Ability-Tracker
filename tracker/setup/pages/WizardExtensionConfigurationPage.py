import tkinter
import webbrowser
from tkinter.font import BOLD, Font
from PIL import Image, ImageDraw, ImageTk
from tracker.setup.WizardPage import WizardPage
from tracker.util.Constants import *
from tracker.actions.KeybindAction import KeybindAction
from tracker.actions.MousebindAction import MousebindAction
from tracker.setup.SetupWizardPageState import SetupWizardPageState


class WizardExtensionConfigurationPage(WizardPage):
    def set_dark_mode(self):
        background_color = self._configuration['wizard-background-color-dark']
        heading_color = self._configuration['wizard-heading-color-dark']
        text_color = self._configuration['wizard-text-color-dark']
        frame_color = self._configuration['wizard-frame-color-dark']
        highlight_color = self._configuration['wizard-highlight-color-dark']
        self._add_data_fp('darkmode', True)

        self._darkmode_button.configure(text="Light Mode", background=background_color, fg=text_color, activebackground=background_color)
        self._github_link_button.configure(fg=text_color, background=background_color, activebackground=background_color)
        self._discord_link_button.configure(fg=text_color, background=background_color, activebackground=background_color)
        self._continue_button.configure(background=background_color, activebackground=background_color)
        self._widget.configure(background=background_color)
        self._action_bar_label.configure(fg=text_color, background=background_color)
        self._main_action_bar.configure(fg=text_color, background=background_color, activebackground=highlight_color, selectcolor='black')
        self._additional_action_bar_1.configure(fg=text_color, background=background_color, activebackground=highlight_color, selectcolor='black')
        self._additional_action_bar_2.configure(fg=text_color, background=background_color, activebackground=highlight_color, selectcolor='black')
        self._additional_action_bar_3.configure(fg=text_color, background=background_color, activebackground=highlight_color, selectcolor='black')
        self._additional_action_bar_4.configure(fg=text_color, background=background_color, activebackground=highlight_color, selectcolor='black')


    def set_light_mode(self):
        background_color = self._configuration['wizard-background-color']
        heading_color = self._configuration['wizard-heading-color']
        text_color = self._configuration['wizard-text-color']
        frame_color = self._configuration['wizard-frame-color']
        highlight_color = self._configuration['wizard-highlight-color']
        self._add_data_fp('darkmode', False)

        self._darkmode_button.configure(text="Dark Mode", background=background_color, fg=text_color, activebackground=background_color)
        self._github_link_button.configure(fg=text_color, background=background_color, activebackground=background_color)
        self._discord_link_button.configure(fg=text_color, background=background_color, activebackground=background_color)
        self._continue_button.configure(background=background_color, activebackground=background_color)
        self._widget.configure(background=background_color)
        self._action_bar_label.configure(fg=text_color, background=background_color)
        self._main_action_bar.configure(fg=text_color, background=background_color, activebackground=heading_color, selectcolor='white')
        self._additional_action_bar_1.configure(fg=text_color, background=background_color, activebackground=heading_color, selectcolor='white')
        self._additional_action_bar_2.configure(fg=text_color, background=background_color, activebackground=heading_color, selectcolor='white')
        self._additional_action_bar_3.configure(fg=text_color, background=background_color, activebackground=heading_color, selectcolor='white')
        self._additional_action_bar_4.configure(fg=text_color, background=background_color, activebackground=heading_color, selectcolor='white')
