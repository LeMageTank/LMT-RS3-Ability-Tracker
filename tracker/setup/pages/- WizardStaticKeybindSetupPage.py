import tkinter
import pyautogui
import webbrowser
import multiprocessing
from PIL import Image, ImageDraw, ImageTk
from tracker.setup.SetupWizardState import SetupWizardState
from tracker.setup.WizardWidget import WizardWidget
from tracker.actions.MousebindAction import MousebindAction
from tracker.actions.KeybindAction import KeybindAction

class WizardKeybindSetupPage(WizardWidget):
    def set_dark_mode(self):
        background_color = self._configuration['wizard-background-color-dark']
        heading_color = self._configuration['wizard-heading-color-dark']
        text_color = self._configuration['wizard-text-color-dark']
        frame_color = '#153363'
        error_color = '#ffa75e'
        self._add_data_fp('darkmode', True)

        self._widget.configure(background=background_color)
        for widget in self._widget_backgrounds:
            widget.configure(background=background_color)
        for widget in self._widget_activebackgrounds:
            widget.configure(activebackground=background_color)
        for widget in self._widget_fg_text:
            widget.configure(fg=text_color)
        for widget in self._widget_fg_heading:
            widget.configure(fg=heading_color)
        for widget in self._widget_frame_colors:
            widget.configure(background=frame_color)

        self._ttk_widget_style.configure('combobox', bg=frame_color, fg=heading_color)

    def set_light_mode(self):
        background_color = self._configuration['wizard-background-color']
        heading_color = self._configuration['wizard-heading-color']
        text_color = self._configuration['wizard-text-color']
        frame_color = '#e6f3fa'
        error_color = '#9c4702'
        self._add_data_fp('darkmode', False)

        self._widget.configure(background=background_color)
        for widget in self._widget_backgrounds:
            widget.configure(background=background_color)
        for widget in self._widget_activebackgrounds:
            widget.configure(activebackground=background_color)
        for widget in self._widget_fg_text:
            widget.configure(fg=text_color)
        for widget in self._widget_fg_heading:
            widget.configure(fg=heading_color)
        for widget in self._widget_frame_colors:
            widget.configure(background=frame_color)

        self._ttk_widget_style.configure('combobox', bg=frame_color, fg=heading_color)

    def change_theme(self):
        self._darkmode = not self._darkmode
        if self._darkmode:
            self.set_light_mode()
        else:
            self.set_dark_mode()

    def update_theme(self):
        if self._darkmode:
            self.set_light_mode()
        else:
            self.set_dark_mode()

    def save_and_contiue(self):
        self._add_data_fp('static-keybinds', self._keybinds)
        self._load_state_fp(SetupWizardState.BINDINGS_ACTION_PROFILE_SETUP_PAGE)

    def initialize_data(self):
        self._action_sets = self._get_data_fp('static-action-sets')
        self._action_sets = ['Action Bar 1', 'Action Bar 2', 'Prayer Book', 'Action Bar 9']
        self._mousebinds = self._get_data_fp('static-mousebinds')
        self._keybinds = self._get_data_fp('static-keybinds')
        if self._keybinds is None:
            self._keybinds = {}
            for action_set, mousebind_list in self._mousebinds.items():
                keybind_list = []
                for mousebind in mousebind_list:
                    keybind = KeybindAction({'action':mousebind.action, 'key':'',
                                             'modifier':''})
                    keybind_list.append(keybind)
                self._keybinds[action_set] = keybind_list
        else:
            for action_set, mousebind_list in self._mousebinds.items():
                if action_set not in self._keybinds.keys():
                    keybind_list = []
                    for mousebind in self._mousebinds[action_set]:
                        keybind = KeybindAction({'action':mousebind.action, 'key':'',
                                                 'modifier':''})
                        keybind_list.append(keybind)
                    self._keybinds[action_set] = keybind_list

    def select_action_set(self, event):
        if len(self._action_set_container.curselection()) == 0:
            return
        self._current_action_set = self._action_sets[self._action_set_container.curselection()[0]]
        self._actions_container.delete(0, self._actions_container.size()-1)
        for i in range(0, len(self._keybinds[self._current_action_set])):
            self._actions_container.insert(i, self._keybinds[self._current_action_set][i])
        self._key_entry.delete(0, tkinter.END)
        self._key_modifier_selection_var.set(KeybindAction.modifier_keys_strings[0])

    def select_action(self, event):
        if len(self._actions_container.curselection()) == 0:
            return
        action = self._actions_container.curselection()[0]
        keybind_action = self._keybinds[self._current_action_set][action]
        self._key_entry.delete(0, tkinter.END)
        self._key_entry.insert(0, keybind_action.key)
        self._key_modifier_selection_var.set(KeybindAction.modifier_keys_strings[0])

    def save_keybind(self):
        if len(self._actions_container.curselection()) == 0:
            return
        action = self._actions_container.curselection()[0]
        action_name = self._keybinds[self._current_action_set][action].action
        key =self._key_entry_var.get()
        modifier = self._key_modifier_selection_var.get()
        self.add_keybind(action_name, key, modifier)

    def add_keybind(self, action_name, key, modifier):
        keybind = keybindAction({'action':action_name, 'key':key, 'modifier': modifier})
        self._keybind_mappings[self._current_action_set].append(keybind)
        
    def get_widget(self):
        self.initialize_data()
        self._set_window_size_fp(width=650, height=600)
        self._widget.configure(highlightthickness=0, width=800, height=600)
        header_font = ('Arial', 16, 'bold')
        text_font = ('Arial', 14)

        self._info_label = tkinter.Label(self._widget, text="Keybind Creator", font=header_font)

        self._continue_button = tkinter.Button(self._widget, text="continue",
                                            font=header_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: self.save_and_contiue)

        self._github_link_button = tkinter.Button(self._widget, text="View on GitHub",
                                            font=text_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: webbrowser.open(self._configuration['github-link']))

        self._discord_link_button = tkinter.Button(self._widget, text="Join the Discord",
                                            font=text_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: webbrowser.open(self._configuration['discord-invite']))

        self._darkmode_button = tkinter.Button(self._widget, text="Dark Mode",
                                            font=text_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: self.change_theme())

        self._action_set_label = tkinter.Label(self._widget, text="Static Action Sets", font=text_font)
        self._action_set_container = tkinter.Listbox(self._widget, width=30, height=25)
        self._action_set_container.bind('<<ListboxSelect>>', self.select_action_set)
        for i in range(len(self._action_sets)):
            self._action_set_container.insert(i, self._action_sets[i])

        self._keybind_label = tkinter.Label(self._widget, text="Keybind", font=text_font)

        self._actions_label = tkinter.Label(self._widget, text="Actions", font=text_font)
        self._actions_container = tkinter.Listbox(self._widget, width=30, height=25)
        self._actions_container.bind('<<ListboxSelect>>', self.select_action)

        self._key_entry_var = tkinter.StringVar()
        self._key_entry = tkinter.Entry(self._widget, textvariable=self._key_entry_var, width=4)
        
        self._ttk_widget_style = tkinter.ttk.Style()
        self._ttk_widget_style.configure('combobox')
        self._key_modifier_selection_var = tkinter.StringVar()
        self._key_modifier_selection = tkinter.ttk.Combobox(self._widget, textvariable=self._key_modifier_selection_var)
        self._key_modifier_selection['values'] = KeybindAction.modifier_keys_strings

        self._keybind_save_button = tkinter.Button(self._widget, text="Save",
                                            font=text_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: self.save_keybind())

        self._info_label.place(x=10, y=20)
        self._continue_button.place(x=500, y=550)
        self._github_link_button.place(x=10, y=550)
        self._discord_link_button.place(x=180, y=550)
        self._darkmode_button.place(x=500, y=20)
        self._action_set_label.place(x=20, y=65)
        self._action_set_container.place(x=20, y=100)
        self._actions_container.place(x=200, y=100)
        self._actions_label.place(x=200, y=65)
        self._keybind_label.place(x=400, y=65)
        self._key_entry.place(x=400, y=100)
        self._key_modifier_selection.place(x=400, y=125)
        self._keybind_save_button.place(x=400, y=150)

        self._widget_backgrounds = [self._info_label, self._continue_button, self._github_link_button,
                                    self._discord_link_button, self._action_set_label, self._darkmode_button,
                                    self._actions_label, self._keybind_label]
        self._widget_activebackgrounds = [self._continue_button, self._github_link_button, self._discord_link_button,
                                          self._darkmode_button, self._keybind_save_button]
        self._widget_fg_text = [self._continue_button, self._github_link_button, self._discord_link_button,
                                self._darkmode_button, self._action_set_container, self._actions_container,
                                self._keybind_save_button]
        self._widget_fg_heading = [self._info_label, self._action_set_label, self._keybind_label, self._key_entry,
                                   self._actions_label]
        self._widget_frame_colors = [self._action_set_container, self._actions_container, self._key_entry,
                                     self._keybind_save_button]
        self._darkmode = self._get_data_fp('darkmode')
        self.change_theme()

        return self._widget
