import tkinter
import pyautogui
import webbrowser
import multiprocessing
from PIL import Image, ImageDraw, ImageTk
from tracker.setup.SetupWizardState import SetupWizardState
from tracker.setup.WizardWidget import WizardWidget
from tracker.util.MousebindActionSelector import run_mousebind_action_selector
from tracker.actions.MousebindAction import MousebindAction

MOUSEBIND_CREATION_DIRECTIONS = """\nRight-Click the center of actions that you would like to add to the static action set `{}` and select the action from the dialog box. Click continue when you've added all of the set's actions.\n"""

class WizardStaticMousebindSetupPage(WizardWidget):
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
        print(self._mousebind_mappings)
        self._set_fullscreen_fp(False)
        self._active = False
        self._mouse_listener_control_queue.put('exit')
        self._add_data_fp('static-mousebinds', self._mousebind_mappings)
        self._load_state_fp(SetupWizardState.STATIC_KEYBINDS_PAGE)

    def initialize_data(self):
        self._action_sets = self._get_data_fp('static-action-sets')
        self._action_sets = ['Action Bar 1', 'Action Bar 2', 'Prayer Book', 'Action Bar 9']
        self._mousebind_mappings = self._get_data_fp('static-mousebinds')
        self._mousebind_mappings = {}
        self._active = True
        for action_set in self._action_sets:
            self._mousebind_mappings[action_set] = []

    def screenshot(self):
        return pyautogui.screenshot()

    def load_action_set_creation_ui(self):
        for child_widget in self._widget.winfo_children():
            child_widget.destroy()

        window_position_x = self._widget.winfo_rootx()
        window_position_y = self._widget.winfo_rooty()
            
        self._screenshot_image = self.screenshot()

        h, w = self._screenshot_image.size
        self._set_window_size_fp(width=w, height=h)
        self._set_fullscreen_fp(True)

        self._fullscreen_image = ImageTk.PhotoImage(self._screenshot_image)
        self._fullscreen_image_label = tkinter.Label(self._widget, image=self._fullscreen_image,
                                                     highlightthickness=10, relief='solid',
                                                     highlightbackground ='#153363', highlightcolor='#153363')
        self._fullscreen_image_label.image = self._fullscreen_image
        self._fullscreen_image_label.pack()

        self._instruction_label_frame = tkinter.Frame(self._widget, width=500, height=100)
        self._instruction_label_frame.propagate(0)
        self._instruction_label = tkinter.Label(self._instruction_label_frame, text=MOUSEBIND_CREATION_DIRECTIONS.format(self._current_action_set),
                                                font=('Arial', 12), background='#153363',fg='white',
                                                wraplength=500, justify='left').pack()
        self._instruction_label_frame.place(x=window_position_x, y=window_position_y)

        self._mousebind_label_widgets = []

        if len(self._remaning_action_sets) > 0:
            self._start_button = tkinter.Button(self._widget, text="Continue",
                                            font=('Arial', 16, 'bold'),
                                            background='#153363',fg='white',
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: self.process_next_action_set())
        else:
            self._start_button = tkinter.Button(self._widget, text="Create Static Keybinds",
                                            font=('Arial', 16, 'bold'),
                                            background='#153363',fg='white',
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: self.save_and_contiue())
        self._start_button.place(x=window_position_x+10, y=window_position_y-25)

        self._widget_backgrounds = []
        self._widgets_fg_text = []
        self._widget_fg_heading = []
        self._widget_activebackgrounds = []
        #self.update_theme()

    def draw_mousebinds(self):
        for widget in self._mousebind_label_widgets:
            widget.destroy()
        self._mousebind_label_widgets = []
        for mousebind in self._mousebind_mappings[self._current_action_set]:
            mousebind_label_frame = tkinter.Frame(self._widget, width=30, height=30,
                                                  background='black')
            mousebind_label_frame.place(x=mousebind.x1, y=mousebind.y1)
            mousebind_label_frame.propagate(0)
            mousebind_label = tkinter.Label(mousebind_label_frame, text=mousebind.action,
                                            font=('Arial', 8), background='black',
                                            fg='white', wraplength=30, justify='left',
                                            height=5, width=5)
            mousebind_label.pack(fill='both', expand=1)
            self._mousebind_label_widgets.append(mousebind_label)
            self._mousebind_label_widgets.append(mousebind_label_frame)

    def process_next_action_set(self):
        self._current_action_set = self._remaning_action_sets.pop()
        self._set_window_size_fp(width=500, height=100)
        self._set_fullscreen_fp(False)
        for child_widget in self._widget.winfo_children():
            child_widget.destroy()
        text_font = ('Arial', 14)
        header_font = ('Arial', 16, 'bold')
        self._directions_label = tkinter.Label(self._widget,
                                               text="Open your game client with\naction set `{}`\nin view".format(
                                                   self._current_action_set),
                                               font=text_font)

        self._continue_button = tkinter.Button(self._widget, text="Continue",
                                            font=header_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: self.load_action_set_creation_ui())
        
        self._widget_backgrounds = [self._directions_label, self._continue_button]
        self._widget_fg_text = [self._directions_label]
        self._widget_fg_heading = [self._continue_button]
        self._widget_activebackgrounds = [self._continue_button]

        self._directions_label.place(x=10, y=20)
        self._continue_button.place(x=300, y=18)
        self.update_theme()

    def initialize_mousebind_creation(self):
        self._remaning_action_sets = self._action_sets.copy()
        self.start_mouse_listener()
        self.process_next_action_set()
        self._widget.master.after(100, self.loop)

    def start_mouse_listener(self):
        self._action_queue = multiprocessing.Queue()
        self._mouse_listener_control_queue = multiprocessing.Queue()
        multiprocessing.Process(target=run_mousebind_action_selector, args=(self._action_queue, self._mouse_listener_control_queue,
                                      self._configuration)).start()

    def loop(self):
        if self._active and self._action_queue.qsize() > 0:
            action = self._action_queue.get()
            self.add_mousebind(action)
            self.draw_mousebinds()
        self._widget.master.after(100, self.loop)

    def add_mousebind(self, action):
        action_name, x, y = action
        mousebind = MousebindAction({'action':action_name, 'x1':x-15, 'y1': y-15,
                    'x2':x+15, 'y2':y+15})
        self._mousebind_mappings[self._current_action_set].append(mousebind)
        
    def get_widget(self):
        self.initialize_data()
        self._set_window_size_fp(width=500, height=100)
        header_font = ('Arial', 16, 'bold')
        text_font = ('Arial', 14)
        self._widget.configure(highlightthickness=0, width=500, height=100)

        self._info_label = tkinter.Label(self._widget, text="Static Mousebind Creator", font=header_font)

        self._start_button = tkinter.Button(self._widget, text="Begin",
                                            font=header_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: self.initialize_mousebind_creation())

        self._info_label.place(x=10, y=20)
        self._start_button.place(x=300, y=18)

        self._widget_backgrounds = [self._info_label, self._start_button]
        self._widget_activebackgrounds = [self._start_button]
        self._widget_fg_text = [self._start_button]
        self._widget_fg_heading = [self._info_label]
        self._darkmode = self._get_data_fp('darkmode')
        self.change_theme()

        return self._widget
