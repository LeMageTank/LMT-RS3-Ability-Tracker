import tkinter
import webbrowser
from tkinter.font import BOLD, Font
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
from tracker.setup.WizardPage import WizardPage
from tracker.util.Constants import *
from tracker.actions.KeybindAction import KeybindAction
from tracker.actions.MousebindAction import MousebindAction
from tracker.setup.SetupWizardPageState import SetupWizardPageState


class WizardDefaultActionBarSetupPage(WizardPage):
    def set_dark_mode(self):
        background_color = self._configuration['wizard-background-color-dark']
        heading_color = self._configuration['wizard-heading-color-dark']
        text_color = self._configuration['wizard-text-color-dark']
        frame_color = self._configuration['wizard-frame-color-dark']
        highlight_color = self._configuration['wizard-highlight-color-dark']
        self._add_data_fp('darkmode', True)

        self._darkmode_button.configure(text='Light Mode')
        for widget in self._text_widgets:
            widget.configure(foreground=text_color)
        for widget in self._heading_widgets:
            widget.configure(foreground=heading_color)
        for widget in self._background_widgets:
            widget.configure(background=background_color)

    def set_light_mode(self):
        background_color = self._configuration['wizard-background-color']
        heading_color = self._configuration['wizard-heading-color']
        text_color = self._configuration['wizard-text-color']
        frame_color = self._configuration['wizard-frame-color']
        highlight_color = self._configuration['wizard-highlight-color']
        self._add_data_fp('darkmode', False)

        self._darkmode_button.configure(text='Dark Mode')
        for widget in self._text_widgets:
            widget.configure(foreground=text_color)
        for widget in self._heading_widgets:
            widget.configure(foreground=heading_color)
        for widget in self._background_widgets:
            widget.configure(background=background_color)

    def change_theme(self):
        self._darkmode = not self._darkmode
        if self._darkmode:
            self.set_light_mode()
        else:
            self.set_dark_mode()
    
    def initialize_data(self):
        self._action_bar_presets = self._get_data_fp('action-bar-presets')
        self._action_bar_metadata = self._get_data_fp('action-bar-metadata')
        self._default_loadout = self._get_data_fp('default-loadout')
        if self._default_loadout is None:
            self._default_loadout = {}
            self._add_data_fp('default-loadout', self._default_loadout)

    def save_and_continue(self):
        for action_bar, action_bar_var, combobox in self._action_bar_comboboxes:
            self._default_loadout[action_bar] = combobox.current()       
        self._load_page_fp(SetupWizardPageState.SAVE_AND_EXIT_PAGE)

    def get_widget(self):
        self._set_window_size_fp(width=525, height=250)
        header_font = ('Arial', 16, 'bold')
        text_font = ('Arial', 14)

        self.initialize_data()

        self._text_widgets = []
        self._heading_widgets = []
        self._background_widgets = []

        self._page_label = tkinter.Label(self._widget, text='Default action bar setup', font=header_font)
        self._page_label.grid(column=0, row=0, columnspan=3, sticky=tkinter.EW)

        active_action_bars = []
        for action_bar, metadata in self._action_bar_metadata.items():
            if metadata['active']:
                active_action_bars.append(action_bar)

        action_bar_preset_ids = []
        for i in range(len(self._action_bar_presets)):
            action_bar_preset_ids.append('{}: {}'.format(i+1, self._action_bar_presets[i]['name']))

        self._action_bar_comboboxes = []
        for i in range(len(active_action_bars)):
            action_bar_var = tkinter.StringVar()
            action_bar_combobox = ttk.Combobox(self._widget, textvariable=action_bar_var)
            action_bar_combobox['values'] = action_bar_preset_ids
            self._action_bar_comboboxes.append((active_action_bars[i], action_bar_var, action_bar_combobox))
            if active_action_bars[i] in self._default_loadout.keys():
                action_bar_var.set(action_bar_preset_ids[self._default_loadout[active_action_bars[i]]])
            action_bar_label = tkinter.Label(self._widget, text=active_action_bars[i], font=text_font)
            action_bar_label.grid(column=0, row=i+1, sticky=tkinter.W, padx=10)
            action_bar_combobox.grid(column=2, row=i+1, sticky=tkinter.W)
            self._text_widgets.append(action_bar_label)
            self._background_widgets.append(action_bar_label)
            
        continue_button_image = Image.open(self._configuration['wizard-continue'])
        self._continue_button_image = ImageTk.PhotoImage(continue_button_image)
        self._continue_button = tkinter.Button(self._widget, image=self._continue_button_image,
                                         command= lambda: self.save_and_continue(),
                                         borderwidth=0, highlightthickness=0)

        self._darkmode_button = tkinter.Button(self._widget, text="Dark Mode",
                                            font=text_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: self.change_theme())

        self._darkmode_button.grid(column=0, row=6, columnspan=1, sticky=tkinter.W)
        self._continue_button.grid(column=1, row=6, columnspan=2, sticky=tkinter.W)

        self._text_widgets.extend([self._page_label])
        self._heading_widgets.extend([self._darkmode_button, self._continue_button])
        self._background_widgets.extend([self._page_label, self._continue_button, self._darkmode_button,
                                         self._widget])

        self._darkmode = self._get_data_fp('darkmode')
        self.change_theme()

        return self._widget

        
