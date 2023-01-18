import tkinter
from PIL import Image, ImageDraw, ImageTk
from tracker.actions.MousebindAction import MousebindAction


class ActionBarTemplateWidget(tkinter.Label):
    def __init__(self, root, configuration, main_bar=False, action_bar_name=''):
        self._is_main_bar = main_bar
        self._action_bar_templates = []
        self._current_action_bar_template = 0
        self.action_bar_name = action_bar_name
        if self._is_main_bar:
            for template in configuration['main-action-bar-templates']:
                self._action_bar_templates.append(ActionBarTemplate(template))
        else:
            for template in configuration['additional-action-bar-templates']:
                self._action_bar_templates.append(ActionBarTemplate(template))
        self._image = ImageTk.PhotoImage(
            self._action_bar_templates[self._current_action_bar_template].image)
        wrap_width = self._image.width() * 0.9
        super().__init__(root, bg='#00D500', bd=0, highlightthickness=0,
                         text=action_bar_name.replace('-', ' '), font=('Arial', 14, 'bold'), fg='red',
                         wraplength=wrap_width, justify='left', image=self._image, compound='center')

    def refresh_template(self):
        self._image = ImageTk.PhotoImage(self._action_bar_templates[self._current_action_bar_template].image)
        wrap_width = self._image.width() * 0.9
        self.configure(image=self._image, wraplength=wrap_width)

    def set_template(self, template_number):
        self._current_action_bar_template = template_number
        self.refresh_template()

    def next_template(self):
        self._current_action_bar_template = (self._current_action_bar_template + 1) % len(self._action_bar_templates)
        self.refresh_template()

    def get_template(self):
        return self._current_action_bar_template

    def generate_action_bar(self, offset_x, offset_y):
        active_template = self._action_bar_templates[self._current_action_bar_template]
        action_bar_slots = []

        for column in range(active_template.num_columns):
            for row in range(active_template.num_rows):
                x1 = offset_x + active_template.x_start + (column * (active_template.column_space + active_template.clickable_region_width))
                y1 = offset_y + active_template.y_start + (row * (active_template.row_space + active_template.clickable_region_height))
                x2 = offset_x + x1 + active_template.clickable_region_width
                y2 = offset_y + y1 + active_template.clickable_region_height
                slot_binding = MousebindAction(x1, y1, x2, y2)
                action_bar_slots.append(slot_binding)
        return action_bar_slots
        

class ActionBarTemplate:
    def __init__(self, template):
        self.file = template['file']
        self.num_rows = template['num-rows']
        self.num_columns = template['num-columns']
        self.x_start = template['x-start']
        self.y_start = template['y-start']
        self.row_space = template['row-space']
        self.column_space = template['column-space']
        self.clickable_region_width = template['clickable-region-width']
        self.clickable_region_height = template['clickable-region-height']
        self.image = Image.open(self.file)

