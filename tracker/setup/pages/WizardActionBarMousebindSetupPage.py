import tkinter
import pyautogui
import webbrowser
import multiprocessing
from PIL import Image, ImageDraw, ImageTk, ImageEnhance
from tracker.setup.WizardPage import WizardPage
from tracker.util.MousebindActionSelector import run_mousebind_action_selector
from tracker.actions.MousebindAction import MousebindAction
from tracker.setup.pages.page_elements.ActionBarTemplate import ActionBarTemplateWidget
from tracker.setup.SetupWizardPageState import SetupWizardPageState


class WizardActionBarMousebindSetupPage(WizardPage):
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

    def initialize_data(self):
        self._action_bars = self._get_data_fp('action-bars')
        active_action_bars = {}
        self._action_bar_metadata = self._get_data_fp('action-bar-metadata')
        for action_bar_name, metadata in self._action_bar_metadata.items():
            if metadata['active']:
                active_action_bars[action_bar_name] = self._action_bars[action_bar_name]
        self._action_bars = active_action_bars
 
    def initialize_action_bar_placement_ui(self):
        for child_widget in self._widget.winfo_children():
            child_widget.destroy()

        window_position_x = self._widget.winfo_rootx()
        window_position_y = self._widget.winfo_rooty()

        self._screenshot_image = pyautogui.screenshot()
        self._screenshot_image = ImageEnhance.Brightness(self._screenshot_image).enhance(0.5)

        h, w = self._screenshot_image.size
        self._set_window_size_fp(width=w, height=h)
        self._set_fullscreen_fp(True)

        self._canvas = tkinter.Canvas(self._widget, width=w, height=h, bd=0, highlightthickness=0)
        self._canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        self._fullscreen_image = ImageTk.PhotoImage(self._screenshot_image)
        self._fullscreen_image_label = tkinter.Label(self._canvas, image=self._fullscreen_image,
                                                     highlightthickness=0, relief='solid',
                                                     highlightbackground ='#153363', highlightcolor='#153363')
        self._fullscreen_image_label.image = self._fullscreen_image
        self._canvas.create_window((0,0), window=self._fullscreen_image_label, anchor='nw')

        self._instruction_box = tkinter.Frame(self._canvas, bg=self._configuration['wizard-frame-color-dark'], highlightthickness=4,
                                              highlightbackground=self._configuration['wizard-text-color-dark'])
        self._instruction_box.bind('<Button-1>', self.button_down_event)
        self._instruction_box.bind('<ButtonRelease-1>', self.button_up_event)
        self._instruction_box.bind('<B1-Motion>', self.move_event)
        
        self._instruction_label = tkinter.Label(self._instruction_box, text="Drag each action bar exactly over their locations on-screen.\nRight click an action bar to change its layout.",
                                                font=('Arial', 12), background='#153363',fg='white', wraplength=500, justify='left')
        self._instruction_label.pack()
        self._instruction_label.parent_widget = self._instruction_box
        self._instruction_label.bind('<Button-1>', lambda e: self.button_down_event(e, affects_parent=True))
        self._instruction_label.bind('<ButtonRelease-1>', self.button_up_event)
        self._instruction_label.bind('<B1-Motion>', self.move_event)
        
        continue_button_image = Image.open(self._configuration['wizard-continue'])
        self._continue_button_image = ImageTk.PhotoImage(continue_button_image)
        self._continue_button = tkinter.Button(self._instruction_box, image=self._continue_button_image,
                                         command= self.save_and_continue,
                                         borderwidth=0, highlightthickness=0, bg=self._configuration['wizard-frame-color-dark'])
        self._continue_button.pack()
        self._canvas.create_window((500,10), window=self._instruction_box, anchor='nw')

        self._action_bar_templates = []
        for action_bar_name, action_bar in self._action_bars.items():
            action_bar_template = ActionBarTemplateWidget(self._canvas, self._configuration, action_bar_name=='main-action-bar', action_bar_name=action_bar_name)
            action_bar_template.set_template(self._action_bar_metadata[action_bar_name]['template-number'])
            x_coord, y_coord = self._action_bar_metadata[action_bar_name]['screen-location']
            if x_coord == 0 and y_coord == 0:
                y_coord = 10 + (len(self._action_bar_templates)*80)
            action_bar_template.canvas_id = self._canvas.create_window((x_coord, y_coord), window=action_bar_template, anchor='nw')
            action_bar_template.bind('<Button-1>', self.button_down_event)
            action_bar_template.bind('<ButtonRelease-1>', self.button_up_event)
            action_bar_template.bind('<B1-Motion>', self.move_event)
            action_bar_template.bind('<Button-3>', self.change_action_bar_template_layout)
            self._action_bar_templates.append(action_bar_template)

        self._widget_backgrounds = []
        self._widgets_fg_text = []
        self._widget_fg_heading = []
        self._widget_activebackgrounds = []

    def button_down_event(self, event, affects_parent=False):
        if not affects_parent:
            self._selected_widget = event.widget
        else:
            self._selected_widget = event.widget.parent_widget
        self._selected_widget.x_offset = event.x
        self._selected_widget.y_offset = event.y

    def button_up_event(self, event):
        self._selected_action_bar_template = None

    def move_event(self, event):
        if not self._selected_widget:
            return
        x = self._widget.winfo_pointerx() - self._widget.winfo_rootx() - self._selected_widget.x_offset
        y = self._widget.winfo_pointery() - self._widget.winfo_rooty() - self._selected_widget.y_offset
        self._selected_widget.place(x=x, y=y)

    def change_action_bar_template_layout(self, event):
        event.widget.next_template()

    def save_and_continue(self):
        for action_bar_template in self._action_bar_templates:
            x1 = action_bar_template.winfo_rootx()
            y1 = action_bar_template.winfo_rooty()
            action_bar_mousebinds = action_bar_template.generate_action_bar(x1, y1)
            for i in range(len(action_bar_mousebinds)):
                self._action_bars[action_bar_template.action_bar_name][i]['mousebind'] = action_bar_mousebinds[i]
            self._action_bar_metadata[action_bar_template.action_bar_name]['screen-location'] = [x1, y1]
            self._action_bar_metadata[action_bar_template.action_bar_name]['template-number'] = action_bar_template.get_template()
        self._set_fullscreen_fp(False)
        self._load_page_fp(SetupWizardPageState.WEAPON_SWITCH_SETUP_PAGE)

    def get_widget(self):
        self.initialize_data()
        self._set_window_size_fp(width=500, height=100)
        header_font = ('Arial', 16, 'bold')
        text_font = ('Arial', 14)
        self._widget.configure(highlightthickness=0, borderwidth=0, padx=0, pady=0, relief=tkinter.FLAT, width=500, height=100)

        self._info_label = tkinter.Label(self._widget, text="Mousebind Creator", font=header_font)

        self._directions_label = tkinter.Label(self._widget, text="Make sure all actions bars are in view.", font=text_font)

        self._start_button = tkinter.Button(self._widget, text="Begin",
                                            font=header_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: self.initialize_action_bar_placement_ui())

        self._info_label.place(x=10, y=20)
        self._directions_label.place(x=10,y=50)
        self._start_button.place(x=390, y=30)

        self._widget_backgrounds = [self._info_label, self._start_button, self._directions_label]
        self._widget_activebackgrounds = [self._start_button]
        self._widget_fg_text = [self._start_button, self._directions_label]
        self._widget_fg_heading = [self._info_label]
        self._darkmode = self._get_data_fp('darkmode')
        self.change_theme()

        return self._widget
