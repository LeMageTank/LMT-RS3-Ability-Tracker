import tkinter
import pyautogui
import webbrowser
import multiprocessing
from PIL import Image, ImageDraw, ImageTk
from tracker.setup.SetupWizardState import SetupWizardState
from tracker.setup.WizardWidget import WizardWidget
from tracker.actions.MousebindAction import MousebindAction
from tracker.actions.KeybindAction import KeybindAction
from tracker.util.Constants import *

class WizardActionBarKeybindSetupPage(WizardWidget):
    def set_dark_mode(self):
        background_color = self._configuration['wizard-background-color-dark']
        heading_color = self._configuration['wizard-heading-color-dark']
        text_color = self._configuration['wizard-text-color-dark']
        frame_color = self._configuration['wizard-frame-color-dark']
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

        self._ttk_widget_style.configure('style.TCombobox', bg=frame_color, fg=heading_color)

    def set_light_mode(self):
        background_color = self._configuration['wizard-background-color']
        heading_color = self._configuration['wizard-heading-color']
        text_color = self._configuration['wizard-text-color']
        frame_color = self._configuration['wizard-frame-color']
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

        self._ttk_widget_style.configure('style.TCombobox', bg=frame_color, fg=heading_color)

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

    def save_and_continue(self):
        for keybind in self._keybinds:
            self._action_bars[keybind[0]][keybind[1]]['keybind'] = KeybindAction(
                {'key':keybind[2].get(), 'modifier':keybind[3].get()})
        self._load_state_fp(SetupWizardState.MOUSEBIND_SETUP_PAGE)

    def initialize_data(self):
        self._action_bars = self._get_data_fp('action-bars')

    def get_widget(self):
        self.initialize_data()
        self._set_window_size_fp(width=425, height=650)
        self._widget.configure(highlightthickness=0, width=425, height=650)
        header_font = ('Arial', 16, 'bold')
        text_font = ('Arial', 14)

        self._info_label = tkinter.Label(self._widget, text="Keybind Creator", font=header_font)

        continue_button_image = Image.open(self._configuration['wizard-continue'])
        self._continue_button_image = ImageTk.PhotoImage(continue_button_image)
        self._continue_button = tkinter.Button(self._widget, image=self._continue_button_image,
                                         command= lambda: self.save_and_continue(),
                                         borderwidth=0, highlightthickness=0)

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

        self._keybind_panel = tkinter.Frame(self._widget, width=550, height=450, highlightthickness=0)

        self._keybind_view = tkinter.Canvas(self._keybind_panel, width=500, highlightthickness=0)
        self._keybind_view_scrollbar = tkinter.Scrollbar(self._keybind_panel, orient=tkinter.VERTICAL)

        self._keybind_list_frame = tkinter.Frame(self._keybind_view)
        self._keybind_view.create_window((0,0), window=self._keybind_list_frame, anchor='nw')

        self._widget_backgrounds = [self._continue_button, self._github_link_button, self._discord_link_button,
                                    self._darkmode_button, self._keybind_view, self._keybind_list_frame, self._info_label,
                                    self._keybind_panel]
        self._widget_activebackgrounds = [self._continue_button, self._github_link_button, self._discord_link_button,
                                          self._darkmode_button, self._keybind_view_scrollbar]
        self._widget_fg_text = [self._github_link_button, self._darkmode_button, self._discord_link_button]
        self._widget_fg_heading = [self._info_label]
        self._widget_frame_colors = [self._keybind_view_scrollbar]
        self._ttk_widget_style = tkinter.ttk.Style()
        self._ttk_widget_style.configure('style.TCombobox', bg='black')

        self._keybinds = []
        row_count = 0
        for action_bar_name, action_bar_contents in self._action_bars.items():
            action_bar_label = tkinter.Label(self._keybind_list_frame, text=action_bar_name,
                font=header_font)
            self._widget_backgrounds.append(action_bar_label)
            self._widget_fg_text.append(action_bar_label)
            action_bar_label.grid(row=row_count, column=0, columnspan=4)
            row_count += 1

            for i in range(len(action_bar_contents)):
                slot_label = tkinter.Label(self._keybind_list_frame, text='Slot {}'.format(str(i+1)),
                    font=text_font)

                key_entry_var = tkinter.StringVar()
                key_entry = tkinter.Entry(self._keybind_list_frame, textvariable=key_entry_var, width=3)
                key_entry_var.set(action_bar_contents[i]['keybind'].primary_key)

                modifier_selector_var = tkinter.StringVar()
                modifier_selector = tkinter.ttk.Combobox(self._keybind_list_frame, textvariable=modifier_selector_var,
                    style='style.TCombobox')
                modifier_selector['values'] = KeybindAction.modifier_keys_strings
                modifier_selector_var.set(action_bar_contents[i]['keybind'].modifier_key)

                slot_label.grid(row=row_count, column=0, padx=10)
                key_entry.grid(row=row_count, column=1, padx=10)
                modifier_selector.grid(row=row_count, column=2, padx=10)

                self._widget_backgrounds.extend([slot_label])
                self._widget_fg_text.extend([slot_label, key_entry])
                self._widget_frame_colors.extend([key_entry, modifier_selector])
                self._keybinds.append((action_bar_name, i, key_entry_var, modifier_selector_var))
                row_count += 1

        self._keybind_list_frame.update()
        self._keybind_view.grid(row=0, column=0, sticky='nsew')
        self._keybind_view_scrollbar.grid(row=0, column=1, sticky='ns')
        self._keybind_view.configure(width=300, height=400)
        self._keybind_view_scrollbar.configure(command=self._keybind_view.yview)
        self._keybind_view.configure(yscrollcommand=self._keybind_view_scrollbar.set,
            scrollregion=self._keybind_view.bbox('all'))

        self._info_label.place(x=115, y=45)
        self._continue_button.place(x=55, y=550)
        self._github_link_button.place(x=40, y=500)
        self._discord_link_button.place(x=205, y=500)
        self._darkmode_button.place(x=10, y=10)
        self._keybind_panel.place(x=50, y=85)

        self._darkmode = self._get_data_fp('darkmode')
        self.change_theme()

        return self._widget
