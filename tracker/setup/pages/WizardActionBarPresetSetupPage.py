import tkinter
from tkinter import ttk
import webbrowser
import json
from tkinter.font import BOLD, Font
from PIL import Image, ImageDraw, ImageTk
from idlelib.tooltip import Hovertip
from tracker.setup.WizardPage import WizardPage
from tracker.setup.pages.page_elements.ActionBarPreset import ActionBarPreset
from tracker.util.Constants import *
from tracker.actions.KeybindAction import KeybindAction
from tracker.actions.MousebindAction import MousebindAction
from tracker.actions.Action import Action
from tracker.setup.SetupWizardPageState import SetupWizardPageState


class WizardActionBarPresetSetupPage(WizardPage):
    def load_actions(self):
        with open(self._configuration['action-info-file'], 'r+') as file:
            loaded_actions = json.loads("".join(file.readlines()))
            actions_list = []
            for action in loaded_actions:
                actions_list.append(Action(action))
            return actions_list

    def load_actions_with_icons(self):
        actions_list = self.load_actions()
        icon_directory = self._configuration['action-icon-directory']
        for action in actions_list:
            action.image = Image.open(icon_directory + action.id + '.png')
        return actions_list

    def fill_action_book(self):
        self.melee_tab = tkinter.Frame(self._action_book, width=600, height=350)
        self.melee_tab.pack(fill='both', expand=True)
        self._melee_image = Image.open(self._configuration['setup-icons']['melee']['default'])
        self._melee_image_selected = Image.open(self._configuration['setup-icons']['melee']['selected'])
        self._melee_image_tk = ImageTk.PhotoImage(self._melee_image)
        self._melee_image_selected_tk = ImageTk.PhotoImage(self._melee_image_selected)
        self._widget_frame_colors.append(self.melee_tab)

        self.magic_tab = tkinter.Frame(self._action_book, width=600, height=350)
        self.magic_tab.pack(fill='both', expand=True)
        self._magic_image = Image.open(self._configuration['setup-icons']['magic']['default'])
        self._magic_image_selected = Image.open(self._configuration['setup-icons']['magic']['selected'])
        self._magic_image_tk = ImageTk.PhotoImage(self._magic_image)
        self._magic_image_selected_tk = ImageTk.PhotoImage(self._magic_image_selected)
        self._widget_frame_colors.append(self.magic_tab)

        self.ranged_tab = tkinter.Frame(self._action_book, width=600, height=350)
        self.ranged_tab.pack(fill='both', expand=True)
        self._ranged_image = Image.open(self._configuration['setup-icons']['ranged']['default'])
        self._ranged_image_selected = Image.open(self._configuration['setup-icons']['ranged']['selected'])
        self._ranged_image_tk = ImageTk.PhotoImage(self._ranged_image)
        self._ranged_image_selected_tk = ImageTk.PhotoImage(self._ranged_image_selected)
        self._widget_frame_colors.append(self.ranged_tab)

        self.defence_constitution_tab = tkinter.Frame(self._action_book, width=600, height=350)
        self.defence_constitution_tab.pack(fill='both', expand=True)
        self._defence_constitution_image = Image.open(self._configuration['setup-icons']['defence-constitution']['default'])
        self._defence_constitution_image_selected = Image.open(self._configuration['setup-icons']['defence-constitution']['selected'])
        self._defence_constitution_image_tk = ImageTk.PhotoImage(self._defence_constitution_image)
        self._defence_constitution_image_selected_tk = ImageTk.PhotoImage(self._defence_constitution_image_selected)
        self._widget_frame_colors.append(self.defence_constitution_tab)

        self.necromancy_tab = tkinter.Frame(self._action_book, width=600, height=350)
        self.necromancy_tab.pack(fill='both', expand=True)
        self._necromancy_image = Image.open(self._configuration['setup-icons']['necromancy']['default'])
        self._necromancy_image_selected = Image.open(self._configuration['setup-icons']['necromancy']['selected'])
        self._necromancy_image_tk = ImageTk.PhotoImage(self._necromancy_image)
        self._necromancy_image_selected_tk = ImageTk.PhotoImage(self._necromancy_image_selected)
        self._widget_frame_colors.append(self.necromancy_tab)

        self.item_tab = tkinter.Frame(self._action_book, width=600, height=350)
        self.item_tab.pack(fill='both', expand=True)
        self._item_image = Image.open(self._configuration['setup-icons']['item']['default'])
        self._item_image_selected = Image.open(self._configuration['setup-icons']['item']['selected'])
        self._item_image_tk = ImageTk.PhotoImage(self._item_image)
        self._item_image_selected_tk = ImageTk.PhotoImage(self._item_image_selected)
        self._widget_frame_colors.append(self.item_tab)

        self.prayer_tab = tkinter.Frame(self._action_book, width=600, height=350)
        self.prayer_tab.pack(fill='both', expand=True)
        self._prayer_image = Image.open(self._configuration['setup-icons']['prayer']['default'])
        self._prayer_image_selected = Image.open(self._configuration['setup-icons']['prayer']['selected'])
        self._prayer_image_tk = ImageTk.PhotoImage(self._prayer_image)
        self._prayer_image_selected_tk = ImageTk.PhotoImage(self._prayer_image_selected)
        self._widget_frame_colors.append(self.prayer_tab)

        self._action_book.add(self.melee_tab, image=self._melee_image_tk)
        self._action_book.add(self.magic_tab, image=self._magic_image_tk)
        self._action_book.add(self.ranged_tab, image=self._ranged_image_tk)
        self._action_book.add(self.necromancy_tab, image=self._necromancy_image_tk)
        self._action_book.add(self.defence_constitution_tab, image=self._defence_constitution_image_tk)
        self._action_book.add(self.item_tab, image=self._item_image_tk)
        self._action_book.add(self.prayer_tab, image=self._prayer_image_tk)

        self._action_book_tab_images = [
            self._melee_image_tk,
            self._magic_image_tk,
            self._ranged_image_tk,
            self._necromancy_image_tk,
            self._defence_constitution_image_tk,
            self._item_image_tk,
            self._prayer_image_tk
        ]

        self._action_book_tab_selected_images = [
            self._melee_image_selected_tk,
            self._magic_image_selected_tk,
            self._ranged_image_selected_tk,
            self._necromancy_image_selected_tk,
            self._defence_constitution_image_selected_tk,
            self._item_image_selected_tk,
            self._prayer_image_selected_tk
        ]

        self._actions_map = {
            'ranged': {},
            'magic': {},
            'melee': {},
            'necromancy': {},
            'defence/constitution': {},
            'item': {},
            'prayer':{}
        }

        for action in self._actions_list:
            tab = self._actions_map[action.tag]
            if action.action_type not in tab.keys():
                tab[action.action_type] = []
            tab[action.action_type].append(action)

        self._image_widgets = []
        for tab_name, tab in [('melee', self.melee_tab), ('magic', self.magic_tab),
            ('ranged', self.ranged_tab), ('necromancy', self.necromancy_tab),
            ('defence/constitution', self.defence_constitution_tab), ('item', self.item_tab),
            ('prayer', self.prayer_tab)]:
            row = 0
            max_icons_per_row = 10

            tab_view = tkinter.Canvas(tab, highlightthickness=0)
            tab_area = tkinter.Frame(tab_view)
            tab_view.create_window((0,0), window=tab_area, anchor='nw')

            tab_scrollbar = tkinter.Scrollbar(tab, orient=tkinter.VERTICAL)

            for tag, action_list in self._actions_map[tab_name].items():
                tag_frame = tkinter.Frame(tab_area)
                tag_frame.grid(row=row, sticky='w')
                self._widget_frame_colors.append(tag_frame)
                row += 1
                label = tkinter.Label(tag_frame, text='{}:'.format(tag.upper()),
                    font=('Arial', 14, 'bold'))
                label.grid(row=0, sticky='w')
                self._widget_frame_colors.append(label)
                self._widget_fg_heading.append(label)
                icon_frame = tkinter.Frame(tag_frame)
                icon_frame.grid(row=1, sticky='w')
                self._widget_frame_colors.append(icon_frame)
                for i, action in enumerate(action_list):
                    image_widget = ImageTk.PhotoImage(action.image)
                    self._image_widgets.append(image_widget)
                    icon = tkinter.Label(icon_frame, image=image_widget)
                    self._widget_frame_colors.append(icon)
                    icon.action = action
                    icon.grid(column=i%max_icons_per_row, row=i//max_icons_per_row)
                    icon.bind('<Button-1>', lambda e: self.button_down_action(e))
                    icon.bind('<ButtonRelease-1>', lambda e: self.button_up_action(e))
                    icon.bind('<B1-Motion>', self.hovered_action_follows_cursor)
                    action_tooltip = Hovertip(icon, action.id, hover_delay=25)

            tab_area.update()
            tab_view.configure(width=360, height=340)
            tab_scrollbar.configure(command=tab_view.yview)
            tab_view.configure(yscrollcommand=tab_scrollbar.set, scrollregion=tab_view.bbox('all'))
            tab_view.grid(row=0, column=0, sticky='w')
            tab_scrollbar.grid(row=0, column=1, sticky='nse')

            self._widget_activebackgrounds.extend([tab_scrollbar])
            self._widget_frame_colors.extend([tab_view, tab_area, tab_scrollbar])

    def action_book_tab_changed(self, event):
        for i, image in enumerate(self._action_book_tab_images):
            self._action_book.tab(i, image=image)
        active_tab_index = self._action_book.index(self._action_book.select())
        self._action_book.tab(active_tab_index,
            image=self._action_book_tab_selected_images[active_tab_index])

    def button_down_action(self, event):
        self._hovered_action = event.widget.action
        self._hovered_action_image = ImageTk.PhotoImage(event.widget.action.image)
        self._hovered_action_widget = tkinter.Label(self._widget, image=self._hovered_action_image,
            background=self._configuration['wizard-background-color-dark'] if self._get_data_fp('darkmode') else self._configuration['wizard-background-color'])
        self._hovered_action_widget.x_offset = event.x
        self._hovered_action_widget.y_offset = event.y
        cursor_x = self._widget.winfo_pointerx() - self._widget.winfo_rootx()
        cursor_y = self._widget.winfo_pointery() - self._widget.winfo_rooty()
        self._hovered_action_widget.place(x=cursor_x-event.x, y=cursor_y-event.y)

    def button_up_action(self, event):
        if self._hovered_action_widget:
            self._hovered_action_widget.destroy()
            self.try_add_action_to_preset(self._hovered_action,
                self._widget.winfo_pointerx(),
                self._widget.winfo_pointery())
        self._hovered_action = None

    def hovered_action_follows_cursor(self, event):
        if not self._hovered_action or not self._hovered_action_widget:
            return
        x = self._widget.winfo_pointerx() - self._widget.winfo_rootx() - self._hovered_action_widget.x_offset
        y = self._widget.winfo_pointery() - self._widget.winfo_rooty() - self._hovered_action_widget.y_offset
        self._hovered_action_widget.place(x=x, y=y)

    def try_add_action_to_preset(self, action, x, y):
        for preset_template in self._action_bar_preset_templates:
            if preset_template.try_add_action_to_preset(x, y, action):
                break

    def set_dark_mode(self):
        background_color = self._configuration['wizard-background-color-dark']
        heading_color = self._configuration['wizard-heading-color-dark']
        text_color = self._configuration['wizard-text-color-dark']
        frame_color = self._configuration['wizard-frame-color-dark']
        highlight_color = self._configuration['wizard-highlight-color-dark']
        self._add_data_fp('darkmode', True)

        self._ttk_widget_style.theme_use('darkmode')
        self._widget.configure(background=background_color)
        self._darkmode_button.configure(text="Light Mode", background=background_color, fg=text_color, activebackground=background_color)
        for widget in self._widget_frame_colors:
            widget.configure(bg=frame_color)
        for widget in self._widget_fg_heading:
            widget.configure(fg=heading_color)
        for widget in self._widget_activebackgrounds:
            widget.configure(activebackground=background_color)
        for widget in self._widget_backgrounds:
            widget.configure(background=background_color)

    def set_light_mode(self):
        background_color = self._configuration['wizard-background-color']
        heading_color = self._configuration['wizard-heading-color']
        text_color = self._configuration['wizard-text-color']
        frame_color = self._configuration['wizard-frame-color']
        highlight_color = self._configuration['wizard-highlight-color']
        self._add_data_fp('darkmode', False)

        self._ttk_widget_style.theme_use('lightmode')
        self._widget.configure(background=background_color)
        self._darkmode_button.configure(text="Dark Mode", background=background_color, fg=text_color, activebackground=background_color)
        for widget in self._widget_frame_colors:
            widget.configure(bg=frame_color)
        for widget in self._widget_fg_heading:
            widget.configure(fg=heading_color)
        for widget in self._widget_activebackgrounds:
            widget.configure(activebackground=background_color)
        for widget in self._widget_backgrounds:
            widget.configure(background=background_color)

    def change_theme(self):
        self._darkmode = not self._darkmode
        if self._darkmode:
            self.set_light_mode()
        else:
            self.set_dark_mode()

    def save_and_continue(self):
        actions_bar_presets_dicts = []
        for action_bar_preset in self._action_bar_preset_templates:
            actions_bar_presets_dicts.append(action_bar_preset.to_dict())
        self._add_data_fp('action-bar-presets', actions_bar_presets_dicts)
        self._load_page_fp(SetupWizardPageState.ACTION_BAR_SETUP_PAGE)

    def get_widget(self):
        self._set_window_size_fp(width=1235, height=400)
        header_font = ('Arial', 16, 'bold')
        text_font = ('Arial', 14)
        self._widget.configure(highlightthickness=0, width=1235, height=400)

        self._ttk_widget_style = tkinter.ttk.Style()
        self._ttk_widget_style.theme_use('default')
        self._widget_backgrounds = []
        self._widget_frame_colors = []
        self._widget_fg_heading = []
        self._widget_activebackgrounds = []

        self._ttk_widget_style.theme_create('darkmode', parent="classic", settings={
                'TNotebook': {
                    'configure':{'background':self._configuration['wizard-background-color-dark'],
                        'tabmargins':[0,0,0,0],
                        "borderwidth": 0
                    }
                },
                'TNotebook.Tab': {
                    'configure':{'background': self._configuration['wizard-background-color-dark'],
                        'relief':'flat',
                        'borderwidth':0,
                        'padding':[2,0]},
                    'map':{'background':[('selected', self._configuration['wizard-background-color-dark'])],
                        'expand': [('selected', [0, 0, 0, 5])]}
                }
            })

        self._ttk_widget_style.theme_create('lightmode', parent="classic", settings={
                'TNotebook': {
                    'configure':{'background':self._configuration['wizard-background-color'],
                        'tabmargins':[0,0,0,0],
                        "borderwidth": 0
                    }
                },
                'TNotebook.Tab': {
                    'configure':{'background': self._configuration['wizard-background-color'],
                        'relief':'flat',
                        'borderwidth':0,
                        'padding':[2,0]},
                    'map':{'background':[('selected', self._configuration['wizard-background-color'])],
                        'expand': [('selected', [0, 0, 0, 5])]}
                }
            })
        
        self._actions_list = self.load_actions_with_icons()
        def get_action(actions_list, action_id):
            for action in actions_list:
                if action.id == action_id:
                    return action
            raise Exception('Unknown action id: ' + action_id)

        self._hovered_action = None
        self._hovered_action_widget = None

        self._action_book = ttk.Notebook(self._widget, width=376, height=400)
        self._action_book.bind('<<NotebookTabChanged>>', self.action_book_tab_changed)
        self.fill_action_book()
        self._action_book.place(x=0, y=0)

        ACTION_BAR_SECTION_HEIGHT = 300
        ACTION_BAR_SECTION_WIDTH = 800

        self._action_bar_frame = tkinter.Frame(self._widget, width=ACTION_BAR_SECTION_WIDTH,
            height=ACTION_BAR_SECTION_HEIGHT)
        self._action_bar_frame.place(x=400, y=10)
        self._action_bar_frame.configure(highlightthickness=0)

        self._action_bar_view = tkinter.Canvas(self._action_bar_frame, width=ACTION_BAR_SECTION_WIDTH,
            height=ACTION_BAR_SECTION_HEIGHT,
            scrollregion=(0,0,475,1000))
        self._action_bar_view.configure(highlightthickness=0)
        self._action_bar_view.grid(row=0, column=0)

        self._action_bar_scrollbar = tkinter.Scrollbar(self._action_bar_frame, orient=tkinter.VERTICAL)
        self._action_bar_scrollbar.grid(row=0, column=1, sticky='ns')

        self._action_bar_area = tkinter.Frame(self._action_bar_view, width=ACTION_BAR_SECTION_WIDTH,
            height=NUM_ACTION_BAR_PRESETS*ActionBarPreset.ACTION_BAR_HEIGHT)
        self._action_bar_view.create_window((0,0), window=self._action_bar_area, anchor='nw')

        self._action_bar_presets = self._get_data_fp('action-bar-presets')
        if self._action_bar_presets is None or len(self._action_bar_presets) == 0:
            self._action_bar_presets = []
            self._add_data_fp('action-bar-presets', self._action_bar_presets)
            for i in range(NUM_ACTION_BAR_PRESETS):
                slots = [[] for i in range(NUM_ACTIONS_SLOTS_PER_ACTION_BAR)]
                preset = {'name': 'Preset-{}'.format(i+1), 'slots': slots}
                self._action_bar_presets.append(preset)
        elif len(self._action_bar_presets) < NUM_ACTION_BAR_PRESETS:
            for i in range(NUM_ACTION_BAR_PRESETS - len(self._action_bar_presets)):
                slots = [[] for i in range(NUM_ACTIONS_SLOTS_PER_ACTION_BAR)]
                preset = {'name': 'Preset-{}'.format(i+1), 'slots': slots}
                self._action_bar_presets.append(preset)
                
        self._action_bar_preset_templates = []
        for i in range(NUM_ACTION_BAR_PRESETS):
            action_bar_preset = ActionBarPreset(x=0,
                y=0+(i*ActionBarPreset.ACTION_BAR_HEIGHT),
                preset_number=i+1, preset_name=self._action_bar_presets[i]['name'],
                root=self._action_bar_area,
                configuration=self._configuration)
            for index, slot in enumerate(self._action_bar_presets[i]['slots']):
                if len(slot) > 0:
                    action_bar_preset.set_action_slot(index, get_action(self._actions_list, slot[0]))
            self._action_bar_preset_templates.append(action_bar_preset)
            self._widget_frame_colors.extend(action_bar_preset.get_widgets_frame())
            self._widget_fg_heading.extend(action_bar_preset.get_widgets_font())

        self._action_bar_view.update()
        self._action_bar_scrollbar.configure(command=self._action_bar_view.yview)
        self._action_bar_view.configure(yscrollcommand=self._action_bar_scrollbar.set,
            scrollregion=self._action_bar_view.bbox('all'))

        self._darkmode_button = tkinter.Button(self._widget, text="Dark Mode",
                                            font=text_font,
                                            borderwidth=0, highlightthickness=0,
                                            command= lambda: self.change_theme())
        self._darkmode_button.place(x=400, y=360)

        continue_button_image = Image.open(self._configuration['wizard-continue'])
        self._continue_button_image = ImageTk.PhotoImage(continue_button_image)
        self._continue_button = tkinter.Button(self._widget, image=self._continue_button_image,
                                 command= self.save_and_continue,
                                 borderwidth=0, highlightthickness=0)
        self._continue_button.place(x=915, y=325)

        self._widget_frame_colors.extend([self._action_bar_frame, self._action_bar_view,
            self._action_bar_scrollbar, self._action_bar_area])
        self._widget_backgrounds.extend([self._continue_button])
        self._widget_activebackgrounds.extend([self._continue_button])
        self._darkmode = self._get_data_fp('darkmode')
        self.change_theme()

        return self._widget
