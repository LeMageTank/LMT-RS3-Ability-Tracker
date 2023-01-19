import tkinter
from PIL import Image, ImageDraw, ImageTk
from tracker.util.Constants import *

class ActionBarPreset:
    SLOT_INDEX = 0
    ACTION_INDEX = 1
    PRESET_SLOT_X_OFFSET = 7
    PRESET_BAR_X_OFFSET = 90
    PRESET_LABEL_Y_OFFSET = 3
    PRESET_NAME_ENTRY_X_OFFSET = 600
    PRESET_SLOT_Y_OFFSET = 4
    SPACE_BETWEEN_SLOTS = 36
    PRESET_HEIGHT = 38
    ACTION_BAR_HEIGHT = 42
    def __init__(self, x, y, preset_number, preset_name, root, configuration):
        self._root = root
        self._configuration = configuration
        self._preset_number = preset_number
        self._slot_width, self._slot_height = self._configuration['preset-action-bar-template-dimensions']
        self._preset_template_image = Image.open(self._configuration['preset-action-bar-template'])
        self._preset_template_tkimage = ImageTk.PhotoImage(self._preset_template_image)
        self._preset_template = tkinter.Label(self._root, image=self._preset_template_tkimage)
        self._preset_template.config(highlightthickness=0, borderwidth=0)
        self._x = x
        self._y = y
        self._preset_template.place(x=self._x+ActionBarPreset.PRESET_BAR_X_OFFSET, y=self._y)
        self._preset_slots = []
        self._action_images = []
        self._preset_name = tkinter.StringVar()
        self._preset_name.set(preset_name)
        self._font_color_widgets = []
        self._frame_color_widgets = []

        preset_number_label = tkinter.Label(self._root, text='Preset {}'.format(preset_number),
            font=('Arial', 11, 'bold'))
        preset_number_label.place(x=ActionBarPreset.PRESET_SLOT_X_OFFSET,
            y=self._y+ActionBarPreset.PRESET_SLOT_Y_OFFSET+ActionBarPreset.PRESET_LABEL_Y_OFFSET)

        preset_custom_name_entry = tkinter.Entry(self._root, textvariable=self._preset_name,
            font=('Arial', 11, 'bold'))
        preset_custom_name_entry.place(x=ActionBarPreset.PRESET_SLOT_X_OFFSET +
            ActionBarPreset.PRESET_NAME_ENTRY_X_OFFSET,
            y=self._y+ActionBarPreset.PRESET_SLOT_Y_OFFSET+ActionBarPreset.PRESET_LABEL_Y_OFFSET)

        self._font_color_widgets.extend([preset_number_label, preset_custom_name_entry])
        self._frame_color_widgets.extend([preset_number_label, preset_custom_name_entry])

        for i in range(NUM_ACTIONS_SLOTS_PER_ACTION_BAR):
            self._action_images.append(None)
            preset_bar_slot = tkinter.Canvas(self._root, width=self._slot_width, height=self._slot_height)
            preset_bar_slot.config(highlightthickness=0)
            preset_bar_slot.place(x=self._x+ActionBarPreset.PRESET_SLOT_X_OFFSET+ActionBarPreset.PRESET_BAR_X_OFFSET
                +(i*ActionBarPreset.SPACE_BETWEEN_SLOTS), y=self._y+ActionBarPreset.PRESET_SLOT_Y_OFFSET)
            self._preset_slots.append((preset_bar_slot, None))
            self._frame_color_widgets.extend([preset_bar_slot])

    def get_widgets_font(self):
        return self._font_color_widgets

    def get_widgets_frame(self):
        return self._frame_color_widgets

    def try_add_action_to_preset(self, x, y, action):
        for i in range(NUM_ACTIONS_SLOTS_PER_ACTION_BAR):
            if self._point_in_slot(x, y, i):
                preset_bar_slot = self._preset_slots[i][ActionBarPreset.SLOT_INDEX]
                preset_bar_slot.slot_number = i
                preset_bar_slot.bind('<ButtonRelease-1>', self._on_slot_clicked)
                self._action_images[i] = ImageTk.PhotoImage(action.image)
                preset_bar_slot.create_image(0,self._slot_height//2+0,
                image=self._action_images[i], anchor=tkinter.W)
                self._preset_slots[i] = (preset_bar_slot, action)
                return True
        return False

    def set_action_slot(self, slot_number, action):
        preset_bar_slot = self._preset_slots[slot_number][ActionBarPreset.SLOT_INDEX]
        preset_bar_slot.slot_number = slot_number
        preset_bar_slot.bind('<ButtonRelease-1>', self._on_slot_clicked)
        self._action_images[slot_number] = ImageTk.PhotoImage(action.image)
        preset_bar_slot.create_image(0,self._slot_height//2+0,
                image=self._action_images[slot_number], anchor=tkinter.W)
        self._preset_slots[slot_number] = (preset_bar_slot, action)

    def to_dict(self):
        action_bar_preset_dict = {}
        action_bar_preset_dict['name'] = self._preset_name.get()
        slots = []
        for preset_bar_slot in self._preset_slots:
            action = preset_bar_slot[ActionBarPreset.ACTION_INDEX]
            if action:
                slots.append([action.id])
            else:
                slots.append([])
        action_bar_preset_dict['slots'] = slots
        return action_bar_preset_dict

    def _on_slot_clicked(self, event):
        preset_slot = event.widget
        preset_slot.delete('all')
        self._preset_slots[preset_slot.slot_number] = (preset_slot, None)

    def _on_slot_hover_exit(self, event):
        pass

    def _point_in_slot(self, x, y, slot):
        x1 = self._preset_template.winfo_rootx() + (slot*ActionBarPreset.SPACE_BETWEEN_SLOTS)
        x2 = self._preset_template.winfo_rootx() + (slot*ActionBarPreset.SPACE_BETWEEN_SLOTS) + self._slot_width
        y1 = self._preset_template.winfo_rooty()
        y2 = self._preset_template.winfo_rooty() + self._slot_height
        if x >= x1 and x <= x2 and y >= y1 and y <= y2:
            return True
        else:
            return False
