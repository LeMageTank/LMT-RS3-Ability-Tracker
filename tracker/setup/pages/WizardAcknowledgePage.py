import tkinter
import webbrowser
from tkinter.font import BOLD, Font
from PIL import Image, ImageDraw, ImageTk
from tracker.setup.WizardPage import WizardPage
from tracker.setup.SetupWizardPageState import SetupWizardPageState

WARNING_MESSAGE="""This program tracks your
mouse and keyboard inputs.
Your data is interpreted
for the operation of the
ability tracker and other
extensions. Your input
data is not shared or
stored."""


class WizardAcknowledgePage(WizardPage):
    def set_dark_mode(self):
        background_color = self._configuration['wizard-background-color-dark']
        heading_color = self._configuration['wizard-heading-color-dark']
        text_color = self._configuration['wizard-text-color-dark']
        self._add_data_fp('darkmode', True)

        self._input_tracking_message.configure(background=background_color, fg=heading_color)
        self._darkmode_button.configure(text="Light Mode", background=background_color, fg=text_color, activebackground=background_color)
        self._control_container.configure(background=background_color)
        self._github_link_button.configure(fg=text_color, background=background_color, activebackground=background_color)
        self._discord_link_button.configure(fg=text_color, background=background_color, activebackground=background_color)
        self._acknowledge_button.configure(background=background_color, activebackground=background_color)

    def set_light_mode(self):
        background_color = self._configuration['wizard-background-color']
        heading_color = self._configuration['wizard-heading-color']
        text_color = self._configuration['wizard-text-color']
        self._add_data_fp('darkmode', False)

        self._input_tracking_message.configure(background=background_color, fg=heading_color)
        self._darkmode_button.configure(text="Dark Mode", background=background_color, fg=text_color, activebackground=background_color)
        self._control_container.configure(background=background_color)
        self._github_link_button.configure(fg=text_color, background=background_color, activebackground=background_color)
        self._discord_link_button.configure(fg=text_color, background=background_color, activebackground=background_color)
        self._acknowledge_button.configure(background=background_color, activebackground=background_color)


    def change_theme(self):
        self._darkmode = not self._darkmode
        if self._darkmode:
            self.set_light_mode()
        else:
            self.set_dark_mode()

    def get_widget(self):
        self._set_window_size_fp(width=800, height=600)
        header_font = ('Arial', 16, 'bold')
        text_font = ('Arial', 14)

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

        self._image_container = tkinter.Label(self._widget, highlightthickness=0, borderwidth=0)
        self._image_container.image = self._background_image
        self._image_container.configure(image=self._background_image)
        self._image_container.configure(highlightthickness=0)
        self._image_container.grid(row=0, column=1, sticky=tkinter.E)

        self._control_container = tkinter.Frame(self._widget, width=400)
        self._control_container.grid(row=0, column=0, sticky=tkinter.NSEW)

        self._input_tracking_message = tkinter.Label(self._control_container,
                                        text=WARNING_MESSAGE, font=header_font)

        self._github_link_button = tkinter.Button(self._control_container, text="View on GitHub",
                                            font=text_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: webbrowser.open(self._configuration['github-link']))

        self._discord_link_button = tkinter.Button(self._control_container, text="Join the Discord",
                                            font=text_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: webbrowser.open(self._configuration['discord-invite']))

        self._darkmode_button = tkinter.Button(self._control_container, text="Dark Mode",
                                            font=text_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: self.change_theme())

        acknowledge_button_image = Image.open(self._configuration['wizard-acknowledge-page-acknowledge'])
        self._acknowledge_button_image = ImageTk.PhotoImage(acknowledge_button_image)
        self._acknowledge_button = tkinter.Button(self._control_container, image=self._acknowledge_button_image,
                                         command= lambda: self._load_page_fp(SetupWizardPageState.ACTION_BAR_PRESET_SETUP_PAGE),
                                         borderwidth=0, highlightthickness=0)


        self._input_tracking_message.place(x=45, y=80)
        self._github_link_button.place(x=40, y=550)
        self._discord_link_button.place(x=200, y=550)
        self._acknowledge_button.place(x=40, y=400)
        self._darkmode_button.place(x=10, y=10)

        self._darkmode = self._get_data_fp('darkmode')
        self.change_theme()

        return self._widget
