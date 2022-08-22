import tkinter
import webbrowser
from tkinter.font import BOLD, Font
from PIL import Image, ImageDraw, ImageTk
from tracker.setup.SetupWizardState import SetupWizardState
from tracker.setup.WizardWidget import WizardWidget


class WizardWelcomePage(WizardWidget):
    def set_dark_mode(self):
        background_color = self._configuration['wizard-background-color-dark']
        heading_color = self._configuration['wizard-heading-color-dark']
        text_color = self._configuration['wizard-text-color-dark']
        self._add_data_fp('darkmode', True)

        self._darkmode_button.configure(text="Light Mode", background=background_color,
                                        fg=text_color, activebackground=background_color)
        self._control_container.configure(background=background_color)
        self._welcome_message.configure(fg=heading_color, background=background_color, activebackground=background_color,
                                        text="LMT's Ability Tracker\r Setup Dark Wizard")
        self._github_link_button.configure(fg=text_color, background=background_color, activebackground=background_color)
        self._discord_link_button.configure(fg=text_color, background=background_color, activebackground=background_color)
        self._start_button.configure(background=background_color, activebackground=background_color)

    def set_light_mode(self):
        background_color = self._configuration['wizard-background-color']
        heading_color = self._configuration['wizard-heading-color']
        text_color = self._configuration['wizard-text-color']
        self._add_data_fp('darkmode', False)

        self._darkmode_button.configure(text="Dark Mode", background=background_color, fg=text_color, activebackground=background_color)
        self._control_container.configure(background=background_color)
        self._welcome_message.configure(fg=heading_color, background=background_color, activebackground=background_color,
                                        text="LMT's Ability Tracker\r Setup Wizard")
        self._github_link_button.configure(fg=text_color, background=background_color, activebackground=background_color)
        self._discord_link_button.configure(fg=text_color, background=background_color, activebackground=background_color)
        self._start_button.configure(background=background_color, activebackground=background_color)
        

    def change_theme(self):
        self._darkmode = not self._darkmode
        if self._darkmode:
            self.set_light_mode()
        else:
            self.set_dark_mode()
        
    def get_widget(self):
        self._set_window_size_fp(width=800, height=600)
        background_color = '#ffffff'
        heading_color = '#3079f0'
        text_color = '#000000'
        header_font = ('Arial', 22, 'bold')
        text_font = ('Arial', 14)
        
        self._widget.configure(background=background_color)
        self._widget.configure(highlightthickness=0)
        self._widget.columnconfigure(0, weight=2)
        self._widget.columnconfigure(1, weight=1)
        
        background_image = Image.open(self._configuration['wizard-welcome-page-background'])
        w, h = background_image.size
        center_w = w//2
        center_h = w//2
        l = center_w - 200
        r = center_w + 200
        t = center_h - 300
        b = center_h + 300
        background_image = background_image.crop((l, t, r, b))
        self._background_image = ImageTk.PhotoImage(background_image)
        
        self._image_container = tkinter.Label(self._widget, background=background_color,
                                              highlightthickness=0, borderwidth=0)
        self._image_container.image = self._background_image
        self._image_container.configure(image=self._background_image)
        self._image_container.configure(highlightthickness=0)
        self._image_container.grid(row=0, column=1, sticky=tkinter.E)
        
        self._control_container = tkinter.Frame(self._widget, background=background_color,
                                          width=400)
        self._control_container.grid(row=0, column=0, sticky=tkinter.NSEW)

        self._welcome_message = tkinter.Label(self._control_container,
                                        text="LMT's Ability Tracker\r Setup Wizard",
                                        fg=heading_color,
                                        bg=background_color,
                                        font=header_font)

        self._github_link_button = tkinter.Button(self._control_container, text="View on GitHub",
                                            font=text_font,
                                            borderwidth=0, highlightthickness=0,
                                            activebackground=background_color,
                                            bg=background_color,
                                            command= lambda: webbrowser.open(self._configuration['github-link']))

        self._discord_link_button = tkinter.Button(self._control_container, text="Join the Discord",
                                            font=text_font,
                                            borderwidth=0, highlightthickness=0,
                                            activebackground=background_color,
                                            bg=background_color,
                                            command= lambda: webbrowser.open(self._configuration['discord-invite']))

        self._darkmode_button = tkinter.Button(self._control_container, text="Dark Mode",
                                            font=text_font,
                                            borderwidth=0, highlightthickness=0,
                                            activebackground=background_color,
                                            bg=background_color,
                                            command= lambda: self.change_theme())

        start_button_image = Image.open(self._configuration['wizard-welcome-page-start'])
        self._start_button_image = ImageTk.PhotoImage(start_button_image)
        self._start_button = tkinter.Button(self._control_container, image=self._start_button_image,
                                         command= lambda: self._load_state_fp(SetupWizardState.ACKNOWLEDGE_PAGE),
                                         borderwidth=0, highlightthickness=0,
                                         activebackground=background_color,
                                         bg=background_color)
        
        
        self._welcome_message.place(x=45, y=80)
        self._github_link_button.place(x=40, y=550)
        self._discord_link_button.place(x=200, y=550)
        self._start_button.place(x=40, y=400)
        self._darkmode_button.place(x=10, y=10)

        self._darkmode = self._get_data_fp('darkmode')
        self.change_theme()
        
        return self._widget
