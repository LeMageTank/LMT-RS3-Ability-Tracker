import tkinter
import webbrowser
from tkinter.font import BOLD, Font
from PIL import Image, ImageDraw, ImageTk
from tracker.setup.SetupWizardState import SetupWizardState
from tracker.setup.WizardWidget import WizardWidget

class WizardStaticActionSetsSetupPage(WizardWidget):
    def set_dark_mode(self):
        background_color = self._configuration['wizard-background-color-dark']
        heading_color = self._configuration['wizard-heading-color-dark']
        text_color = self._configuration['wizard-text-color-dark']
        frame_color = '#153363'
        error_color = '#ffa75e'
        self._add_data_fp('darkmode', True)

        self._darkmode_button.configure(text="Light Mode", background=background_color, fg=text_color, activebackground=background_color)
        self._github_link_button.configure(fg=text_color, background=background_color, activebackground=background_color)
        self._discord_link_button.configure(fg=text_color, background=background_color, activebackground=background_color)
        self._continue_button.configure(background=background_color, activebackground=background_color)
        self._widget.configure(background=background_color)
        self._action_set_container.configure(fg=text_color, background=frame_color)
        self._action_set_label.configure(fg=text_color, background=background_color)
        self._action_set_name_entry.configure(fg=text_color, background=frame_color)
        self._error_label.configure(fg=error_color, background=background_color)
        self._add_action_set_button.configure(fg=text_color, background=background_color, activebackground=frame_color)
        self._clear_action_sets_button.configure(fg=text_color, background=background_color, activebackground=frame_color)
        self._delete_action_set_button.configure(fg=text_color, background=background_color, activebackground=frame_color)

    def set_light_mode(self):
        background_color = self._configuration['wizard-background-color']
        heading_color = self._configuration['wizard-heading-color']
        text_color = self._configuration['wizard-text-color']
        frame_color = '#e6f3fa'
        error_color = '#9c4702'
        self._add_data_fp('darkmode', False)

        self._darkmode_button.configure(text="Dark Mode", background=background_color, fg=text_color, activebackground=background_color)
        self._github_link_button.configure(fg=text_color, background=background_color, activebackground=background_color)
        self._discord_link_button.configure(fg=text_color, background=background_color, activebackground=background_color)
        self._continue_button.configure(background=background_color, activebackground=background_color)
        self._widget.configure(background=background_color)
        self._action_set_container.configure(fg=text_color, background=frame_color)
        self._action_set_label.configure(fg=text_color, background=background_color)
        self._action_set_name_entry.configure(fg=text_color, background=frame_color)
        self._error_label.configure(fg=error_color, background=background_color)
        self._add_action_set_button.configure(fg=text_color, background=background_color, activebackground=frame_color)
        self._clear_action_sets_button.configure(fg=text_color, background=background_color, activebackground=frame_color)
        self._delete_action_set_button.configure(fg=text_color, background=background_color, activebackground=frame_color)

    def change_theme(self):
        self._darkmode = not self._darkmode
        if self._darkmode:
            self.set_light_mode()
        else:
            self.set_dark_mode()

    def save_and_continue(self):
        self._add_data_fp('static-action-sets', self._action_sets)
        self._load_state_fp(SetupWizardState.STATIC_MOUSEBINDS_PAGE)

    def initialize_data(self):
        #Load the saved data if it exists
        self._action_sets = []

    def add_action_set(self):
        set_name = self._action_set_name_var.get()
        if len(set_name) == 0 or set_name in self._action_sets:
            self._error_label.configure(text='ERROR: Duplicate\nAction Set Names')
            return
        self._action_sets.append(set_name)
        self._action_set_name_var.set('')
        self.update_action_set_container()

    def update_action_set_container(self):
        self._action_set_container.delete(0, self._action_set_container.size()-1)
        for i in range(len(self._action_sets)):
            self._action_set_container.insert(i, self._action_sets[i])
        self._error_label.configure(text='')

    def remove_action_set(self):
        try:
            selected_action_set = self._action_set_container.curselection()[0]
            del self._action_sets[selected_action_set]
            self.update_action_set_container()
        except:
            self._error_label.configure(text='ERROR: Could not remove\naction set')

    def clear_action_sets(self):
        self._action_sets = []
        self.update_action_set_container()
        
    def get_widget(self):
        self.initialize_data()
        self._set_window_size_fp(width=700, height=670)
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

        self._action_set_label = tkinter.Label(self._widget, text="Static Action Sets", font=text_font)
        self._action_set_container = tkinter.Listbox(self._widget, width=50, height=25)

        self._action_set_name_var = tkinter.StringVar()
        self._action_set_name_entry = tkinter.Entry(self._widget, textvariable=self._action_set_name_var,
                                                    font=text_font)

        self._add_action_set_button = tkinter.Button(self._widget, text="Add",
                                            font=text_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: self.add_action_set())

        self._clear_action_sets_button = tkinter.Button(self._widget, text="Clear",
                                            font=text_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: self.clear_action_sets())

        self._delete_action_set_button = tkinter.Button(self._widget, text="Delete",
                                            font=text_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: self.remove_action_set())

      
        self._github_link_button.place(x=40, y=610)
        self._discord_link_button.place(x=200, y=610)
        self._continue_button.place(x=380, y=590)
        self._darkmode_button.place(x=10, y=10)
        self._action_set_container.place(x=50, y=120)
        self._action_set_label.place(x=50,y=90)
        self._action_set_name_entry.place(x=400, y=120)
        self._add_action_set_button.place(x=400, y=150)
        self._clear_action_sets_button.place(x=50, y=525)
        self._delete_action_set_button.place(x=120, y=525)
        self._error_label.place(x=400, y=200)
        
        self._darkmode = self._get_data_fp('darkmode')
        self.change_theme()
        
        return self._widget
