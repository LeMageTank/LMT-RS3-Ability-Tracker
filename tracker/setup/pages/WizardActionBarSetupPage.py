import tkinter
import webbrowser
from tkinter.font import BOLD, Font
from PIL import Image, ImageDraw, ImageTk
from tracker.setup.WizardPage import WizardPage
from tracker.util.Constants import *
from tracker.actions.KeybindAction import KeybindAction
from tracker.actions.MousebindAction import MousebindAction
from tracker.setup.SetupWizardPageState import SetupWizardPageState


class WizardActionBarSetupPage(WizardPage):
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

    def change_theme(self):
        self._darkmode = not self._darkmode
        if self._darkmode:
            self.set_light_mode()
        else:
            self.set_dark_mode()

    def create_action_bar(self):
        action_bar = []
        for i in range(NUM_ACTIONS_SLOTS_PER_ACTION_BAR):
            action_bar.append({'mousebind': MousebindAction(0, 0, 0, 0),
                'keybind': KeybindAction({'key':'','modifier':''})})
        return action_bar

    def save_and_continue(self):
        self._action_bar_metadata['main-action-bar']['active'] = (self._main_action_bar_var.get() == 1)
        self._action_bar_metadata['additional-action-bar-1']['active'] = (self._additional_action_bar_1_var.get() == 1)
        self._action_bar_metadata['additional-action-bar-2']['active'] = (self._additional_action_bar_2_var.get() == 1)
        self._action_bar_metadata['additional-action-bar-3']['active'] = (self._additional_action_bar_3_var.get() == 1)
        self._action_bar_metadata['additional-action-bar-4']['active'] = (self._additional_action_bar_4_var.get() == 1)
        self._load_page_fp(SetupWizardPageState.KEYBIND_SETUP_PAGE)

    def get_widget(self):
        self._set_window_size_fp(width=450, height=500)
        header_font = ('Arial', 16, 'bold')
        text_font = ('Arial', 14)
        self._widget.configure(highlightthickness=0, width=1280, height=720)

        self._error_label = tkinter.Label(self._widget, text="", font=header_font)

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

        continue_button_image = Image.open(self._configuration['wizard-continue'])
        self._continue_button_image = ImageTk.PhotoImage(continue_button_image)
        self._continue_button = tkinter.Button(self._widget, image=self._continue_button_image,
                                         command= lambda: self.save_and_continue(),
                                         borderwidth=0, highlightthickness=0)

        self._action_bar_label = tkinter.Label(self._widget, text="Select which action bars that you have active", font=text_font)

        self._main_action_bar_var = tkinter.IntVar()
        self._main_action_bar = tkinter.Checkbutton(self._widget, text='Main Action Bar',variable=self._main_action_bar_var, onvalue=1, offvalue=0,
                                                    font=text_font)

        self._additional_action_bar_1_var = tkinter.IntVar()
        self._additional_action_bar_1 = tkinter.Checkbutton(self._widget, text='Additional Action Bar 1',variable=self._additional_action_bar_1_var,
                                                       onvalue=1, offvalue=0, font=text_font)

        self._additional_action_bar_2_var = tkinter.IntVar()
        self._additional_action_bar_2 = tkinter.Checkbutton(self._widget, text='Additional Action Bar 2',variable=self._additional_action_bar_2_var,
                                                       onvalue=1, offvalue=0, font=text_font)

        self._additional_action_bar_3_var = tkinter.IntVar()
        self._additional_action_bar_3 = tkinter.Checkbutton(self._widget, text='Additional Action Bar 3',variable=self._additional_action_bar_3_var,
                                                       onvalue=1, offvalue=0, font=text_font)

        self._additional_action_bar_4_var = tkinter.IntVar()
        self._additional_action_bar_4 = tkinter.Checkbutton(self._widget, text='Additional Action Bar 4',variable=self._additional_action_bar_4_var,
                                                       onvalue=1, offvalue=0, font=text_font)

        self._action_bar_metadata = self._get_data_fp('action-bar-metadata')
        if self._action_bar_metadata is None:
            self._action_bar_metadata = {}
            self._add_data_fp('action-bar-metadata', self._action_bar_metadata)
        action_bar_names = ['main-action-bar', 'additional-action-bar-1', 'additional-action-bar-2', 'additional-action-bar-3',
                            'additional-action-bar-4']
        for action_bar_name in action_bar_names:
            if action_bar_name not in self._action_bar_metadata.keys():
                self._action_bar_metadata[action_bar_name] = {'active': True, 'screen-location':[0,0], 'template-number': 0}
        self._main_action_bar_var.set(1) if self._action_bar_metadata['main-action-bar'] else self._main_action_bar_var.set(0)
        self._additional_action_bar_1_var.set(1) if self._action_bar_metadata['additional-action-bar-1']['active'] else self._additional_action_bar_1_var.set(0)
        self._additional_action_bar_2_var.set(1) if self._action_bar_metadata['additional-action-bar-2']['active'] else self._additional_action_bar_2_var.set(0)
        self._additional_action_bar_3_var.set(1) if self._action_bar_metadata['additional-action-bar-3']['active'] else self._additional_action_bar_3_var.set(0)
        self._additional_action_bar_4_var.set(1) if self._action_bar_metadata['additional-action-bar-4']['active'] else self._additional_action_bar_4_var.set(0)
        

        self._github_link_button.place(x=40, y=325)
        self._discord_link_button.place(x=200, y=325)
        self._continue_button.place(x=40, y=390)
        self._darkmode_button.place(x=10, y=10)
        self._action_bar_label.place(x=50,y=90)
        self._main_action_bar.place(x=50, y=120)
        self._additional_action_bar_1.place(x=50, y=150)
        self._additional_action_bar_2.place(x=50, y=180)
        self._additional_action_bar_3.place(x=50, y=210)
        self._additional_action_bar_4.place(x=50, y=240)

        self._darkmode = self._get_data_fp('darkmode')
        self.change_theme()

        return self._widget
