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


class WizardWeaponSwitchSetupPage(WizardPage):
    def set_dark_mode(self):
        background_color = self._configuration['wizard-background-color-dark']
        heading_color = self._configuration['wizard-heading-color-dark']
        text_color = self._configuration['wizard-text-color-dark']
        frame_color = self._configuration['wizard-frame-color-dark']
        highlight_color = self._configuration['wizard-highlight-color-dark']
        self._add_data_fp('darkmode', True)

        self._main_action_bar_bind_checkbox.configure(selectcolor=frame_color)
        self._additional_action_bar_1_bind_checkbox.configure(selectcolor=frame_color)
        self._additional_action_bar_2_bind_checkbox.configure(selectcolor=frame_color)
        self._additional_action_bar_3_bind_checkbox.configure(selectcolor=frame_color)
        self._additional_action_bar_4_bind_checkbox.configure(selectcolor=frame_color)

        for widget in self._font_color:
            widget.configure(foreground=text_color)
        for widget in self._heading_color:
            widget.configure(foreground=heading_color)
        for widget in self._background_color:
            widget.configure(background=background_color)
        for widget in self._frame_color:
            widget.configure(background=frame_color)
        for widget in self._highlight_color:
            widget.configure(activebackground=highlight_color)
        self._darkmode_button.configure(text='Light Mode')

    def set_light_mode(self):
        background_color = self._configuration['wizard-background-color']
        heading_color = self._configuration['wizard-heading-color']
        text_color = self._configuration['wizard-text-color']
        frame_color = self._configuration['wizard-frame-color']
        highlight_color = self._configuration['wizard-highlight-color']
        self._add_data_fp('darkmode', False)

        self._main_action_bar_bind_checkbox.configure(selectcolor=frame_color)
        self._additional_action_bar_1_bind_checkbox.configure(selectcolor=frame_color)
        self._additional_action_bar_2_bind_checkbox.configure(selectcolor=frame_color)
        self._additional_action_bar_3_bind_checkbox.configure(selectcolor=frame_color)
        self._additional_action_bar_4_bind_checkbox.configure(selectcolor=frame_color)

        for widget in self._font_color:
            widget.configure(foreground=text_color)
        for widget in self._heading_color:
            widget.configure(foreground=heading_color)
        for widget in self._background_color:
            widget.configure(background=background_color)
        for widget in self._frame_color:
            widget.configure(background=frame_color)
        for widget in self._highlight_color:
            widget.configure(activebackground=highlight_color)
        self._darkmode_button.configure(text='Dark Mode')

    def change_theme(self):
        self._darkmode = not self._darkmode
        if self._darkmode:
            self.set_light_mode()
        else:
            self.set_dark_mode()

    def initialize_data(self):
        self._action_bar_preset_names = ['']
        action_bar_presets = self._get_data_fp('action-bar-presets')
        for i in range(len(action_bar_presets)):
            self._action_bar_preset_names.append('({}) {}'.format(i+1, action_bar_presets[i]['name']))

        self._weapon_switches = self._get_data_fp('weapon-switches')
        if self._weapon_switches is None:
            self._weapon_switches = {}
            self._add_data_fp('weapon-switches', self._weapon_switches)

    def save_and_continue(self):
        self.save_current_configuration()
        self._load_page_fp(SetupWizardPageState.DEFAULT_ACTION_BAR_PRESET_SETUP_PAGE)

    def save_current_configuration(self):
        weapon_switch_config = {}
        if self._main_action_bar_bind_var.get() == 1:
            if self._main_action_bar_combobox.current() != 0:
                weapon_switch_config['main-action-bar'] = (self._main_action_bar_combobox.current()-1)
        if self._additional_action_bar_1_bind_var.get() == 1:
            if self._additional_action_bar_1_combobox.current() != 0:
                weapon_switch_config['additional-action-bar-1'] = (self._additional_action_bar_1_combobox.current()-1)
        if self._additional_action_bar_2_bind_var.get() == 1:
            if self._additional_action_bar_2_combobox.current() != 0:
                weapon_switch_config['additional-action-bar-2'] = (self._additional_action_bar_1_combobox.current()-1)
        if self._additional_action_bar_3_bind_var.get() == 1:
            if self._additional_action_bar_3_combobox.current() != 0:
                weapon_switch_config['additional-action-bar-3'] = (self._additional_action_bar_1_combobox.current()-1)
        if self._additional_action_bar_4_bind_var.get() == 1:
            if self._additional_action_bar_4_combobox.current() != 0:
                weapon_switch_config['additional-action-bar-4'] = (self._additional_action_bar_1_combobox.current()-1)
        if len(weapon_switch_config.keys()) > 0:
            self._weapon_switches[self._selected_weapon_class] = weapon_switch_config

    def clear_current_configuration(self):
        self._main_action_bar_bind_var.set(0)
        self._main_action_bar_combobox_var.set(self._action_bar_preset_names[0])
        self._additional_action_bar_1_bind_var.set(0)
        self._additional_action_bar_1_combobox_var.set(self._action_bar_preset_names[0])
        self._additional_action_bar_2_bind_var.set(0)
        self._additional_action_bar_2_combobox_var.set(self._action_bar_preset_names[0])
        self._additional_action_bar_3_bind_var.set(0)
        self._additional_action_bar_3_combobox_var.set(self._action_bar_preset_names[0])
        self._additional_action_bar_4_bind_var.set(0)
        self._additional_action_bar_4_combobox_var.set(self._action_bar_preset_names[0])

    def load_configuration(self):
        for action_bar_name, preset_index in self._weapon_switches[self._selected_weapon_class].items():
            match action_bar_name:
                case 'main-action-bar':
                    self._main_action_bar_bind_var.set(1)
                    self._main_action_bar_combobox_var.set(self._action_bar_preset_names[preset_index+1])
                case 'additional-action-bar-1':
                    self._additional_action_bar_1_bind_var.set(1)
                    self._additional_action_bar_1_combobox_var.set(self._action_bar_preset_names[preset_index+1])
                case 'additional-action-bar-2':
                    self._additional_action_bar_2_bind_var.set(1)
                    self._additional_action_bar_2_combobox_var.set(self._action_bar_preset_names[preset_index+1])
                case 'additional-action-bar-3':
                    self._additional_action_bar_3_bind_var.set(1)
                    self._additional_action_bar_3_combobox_var.set(self._action_bar_preset_names[preset_index+1])
                case 'additional-action-bar-4':
                    self._additional_action_bar_4_bind_var.set(1)
                    self._additional_action_bar_4_combobox_var.set(self._action_bar_preset_names[preset_index+1])

    def change_weapon_class_event_handler(self, event):
        if len(self._weapon_class_selection_box.curselection()) > 0:
            if self._selected_weapon_class is not None:
                self.save_current_configuration()
            self.clear_current_configuration()
            self._selected_weapon_class = self._weapon_classes[self._weapon_class_selection_box.curselection()[0]]
            if self._selected_weapon_class in self._weapon_switches.keys():
                self.load_configuration()

    def get_widget(self):
        self._set_window_size_fp(width=640, height=300)
        header_font = ('Arial', 16, 'bold')
        text_font = ('Arial', 14)

        self.initialize_data()
        self._weapon_classes = self._configuration['profile-types']
        self._selected_weapon_class = None

        self._page_label = tkinter.Label(self._widget, text='Weapon switch action bar binding setup', font=header_font)
        self._weapon_class_label = tkinter.Label(self._widget, text='Weapon Class', font=text_font)
        self._action_bar_label = tkinter.Label(self._widget, text='Action Bar', font=text_font)
        self._preset_label = tkinter.Label(self._widget, text='Preset', font=text_font)

        self._weapon_class_selection_box = tkinter.Listbox(self._widget)
        self._weapon_class_selection_box.bind('<<ListboxSelect>>', self.change_weapon_class_event_handler)
        for i, weapon_class in enumerate(self._weapon_classes):
            self._weapon_class_selection_box.insert(i, weapon_class)

        self._main_action_bar_bind_var = tkinter.IntVar()
        self._main_action_bar_bind_checkbox = tkinter.Checkbutton(self._widget, text='Bind',variable=self._main_action_bar_bind_var,
                                                       onvalue=1, offvalue=0, font=text_font, fg='black')

        self._additional_action_bar_1_bind_var = tkinter.IntVar()
        self._additional_action_bar_1_bind_checkbox = tkinter.Checkbutton(self._widget, text='Bind',variable=self._additional_action_bar_1_bind_var,
                                                       onvalue=1, offvalue=0, font=text_font, fg='black')

        self._additional_action_bar_2_bind_var = tkinter.IntVar()
        self._additional_action_bar_2_bind_checkbox = tkinter.Checkbutton(self._widget, text='Bind',variable=self._additional_action_bar_2_bind_var,
                                                       onvalue=1, offvalue=0, font=text_font, fg='black')

        self._additional_action_bar_3_bind_var = tkinter.IntVar()
        self._additional_action_bar_3_bind_checkbox = tkinter.Checkbutton(self._widget, text='Bind',variable=self._additional_action_bar_3_bind_var,
                                                       onvalue=1, offvalue=0, font=text_font, fg='black')

        self._additional_action_bar_4_bind_var = tkinter.IntVar()
        self._additional_action_bar_4_bind_checkbox = tkinter.Checkbutton(self._widget, text='Bind',variable=self._additional_action_bar_4_bind_var,
                                                       onvalue=1, offvalue=0, font=text_font, fg='black')

        self._main_action_bar_label = tkinter.Label(self._widget, text='Main Action Bar', font=text_font)
        self._additional_action_bar_1_label = tkinter.Label(self._widget, text='Additional Action Bar 1', font=text_font)
        self._additional_action_bar_2_label = tkinter.Label(self._widget, text='Additional Action Bar 2', font=text_font)
        self._additional_action_bar_3_label = tkinter.Label(self._widget, text='Additional Action Bar 3', font=text_font)
        self._additional_action_bar_4_label = tkinter.Label(self._widget, text='Additional Action Bar 4', font=text_font)

        self._main_action_bar_combobox_var = tkinter.StringVar()
        self._main_action_bar_combobox = ttk.Combobox(self._widget, textvariable=self._main_action_bar_combobox_var)
        self._main_action_bar_combobox['values'] = self._action_bar_preset_names

        self._additional_action_bar_1_combobox_var = tkinter.StringVar()
        self._additional_action_bar_1_combobox = ttk.Combobox(self._widget, textvariable=self._additional_action_bar_1_combobox_var)
        self._additional_action_bar_1_combobox['values'] = self._action_bar_preset_names

        self._additional_action_bar_2_combobox_var = tkinter.StringVar()
        self._additional_action_bar_2_combobox = ttk.Combobox(self._widget, textvariable=self._additional_action_bar_2_combobox_var)
        self._additional_action_bar_2_combobox['values'] = self._action_bar_preset_names

        self._additional_action_bar_3_combobox_var = tkinter.StringVar()
        self._additional_action_bar_3_combobox = ttk.Combobox(self._widget, textvariable=self._additional_action_bar_3_combobox_var)
        self._additional_action_bar_3_combobox['values'] = self._action_bar_preset_names

        self._additional_action_bar_4_combobox_var = tkinter.StringVar()
        self._additional_action_bar_4_combobox = ttk.Combobox(self._widget, textvariable=self._additional_action_bar_4_combobox_var)
        self._additional_action_bar_4_combobox['values'] = self._action_bar_preset_names

        continue_button_image = Image.open(self._configuration['wizard-continue'])
        self._continue_button_image = ImageTk.PhotoImage(continue_button_image)
        self._continue_button = tkinter.Button(self._widget, image=self._continue_button_image,
                                         command= lambda: self.save_and_continue(),
                                         borderwidth=0, highlightthickness=0)

        self._darkmode_button = tkinter.Button(self._widget, text="Dark Mode",
                                            font=text_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: self.change_theme())

        self._page_label.grid(row=0, column=0, columnspan=4, sticky=tkinter.EW)
        self._weapon_class_label.grid(row=1, column=0, sticky=tkinter.EW)
        self._action_bar_label.grid(row=1, column=1, sticky=tkinter.EW)
        self._preset_label.grid(row=1, column=3, sticky=tkinter.EW)
        
        self._weapon_class_selection_box.grid(row=2, column=0, rowspan=5, sticky=tkinter.NW)

        self._main_action_bar_label.grid(row=2, column=1, sticky=tkinter.NW)
        self._additional_action_bar_1_label.grid(row=3, column=1, sticky=tkinter.NW)
        self._additional_action_bar_2_label.grid(row=4, column=1, sticky=tkinter.NW)
        self._additional_action_bar_3_label.grid(row=5, column=1, sticky=tkinter.NW)
        self._additional_action_bar_4_label.grid(row=6, column=1, sticky=tkinter.NW)
        
        self._main_action_bar_bind_checkbox.grid(row=2, column=2, sticky=tkinter.NW)
        self._additional_action_bar_1_bind_checkbox.grid(row=3, column=2, sticky=tkinter.NW)
        self._additional_action_bar_2_bind_checkbox.grid(row=4, column=2, sticky=tkinter.NW)
        self._additional_action_bar_3_bind_checkbox.grid(row=5, column=2, sticky=tkinter.NW)
        self._additional_action_bar_4_bind_checkbox.grid(row=6, column=2, sticky=tkinter.NW)
        
        self._main_action_bar_combobox.grid(row=2, column=3, sticky=tkinter.NW)
        self._additional_action_bar_1_combobox.grid(row=3, column=3, sticky=tkinter.NW)
        self._additional_action_bar_2_combobox.grid(row=4, column=3, sticky=tkinter.NW)
        self._additional_action_bar_3_combobox.grid(row=5, column=3, sticky=tkinter.NW)
        self._additional_action_bar_4_combobox.grid(row=6, column=3, sticky=tkinter.NW)

        self._darkmode_button.grid(row=7, column=0, sticky=tkinter.NW)
        self._continue_button.grid(row=7, column=2, columnspan=2, sticky=tkinter.NW)

        self._font_color = [self._additional_action_bar_1_label, self._additional_action_bar_2_label, self._additional_action_bar_3_label,
                            self._additional_action_bar_4_label, self._main_action_bar_label]
        self._heading_color = [self._page_label, self._darkmode_button, self._weapon_class_label, self._action_bar_label, self._preset_label,
                               self._main_action_bar_bind_checkbox, self._additional_action_bar_1_bind_checkbox,
                               self._additional_action_bar_2_bind_checkbox, self._additional_action_bar_3_bind_checkbox,
                               self._additional_action_bar_4_bind_checkbox]
        self._background_color = [self._widget, self._darkmode_button, self._continue_button, self._main_action_bar_combobox,
                             self._additional_action_bar_1_combobox, self._additional_action_bar_2_combobox,
                             self._additional_action_bar_3_combobox, self._additional_action_bar_4_combobox,
                             self._weapon_class_label, self._action_bar_label, self._preset_label, self._main_action_bar_label,
                             self._additional_action_bar_1_label, self._additional_action_bar_2_label, self._additional_action_bar_3_label,
                             self._additional_action_bar_4_label, self._main_action_bar_bind_checkbox,
                             self._additional_action_bar_1_bind_checkbox, self._additional_action_bar_2_bind_checkbox,
                             self._additional_action_bar_3_bind_checkbox, self._additional_action_bar_4_bind_checkbox,
                             self._page_label]
        self._frame_color = []
        self._highlight_color = [self._main_action_bar_bind_checkbox, self._additional_action_bar_1_bind_checkbox,
                             self._additional_action_bar_2_bind_checkbox, self._additional_action_bar_3_bind_checkbox,
                             self._additional_action_bar_4_bind_checkbox]

        self._darkmode = self._get_data_fp('darkmode')
        self.change_theme()
        self._weapon_class_selection_box.select_set(0)
        self._weapon_class_selection_box.event_generate('<<ListboxSelect>>')

        return self._widget

