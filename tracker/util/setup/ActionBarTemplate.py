import tkinter
from PIL import Image, ImageDraw, ImageTk


class ActionBarTemplateLabel(tkinter.Label):
    def __init__(self, root, configuration, main_bar=False):
        self._is_main_bar = main_bar
        self._action_bar_templates = []
        self._current_action_bar_template = 0
        if self._is_main_bar:
            for template in configuration['main-action-bar-templates']:
                self._action_bar_templates.append(ActionBarTemplate(template))
        else:
            for template in configuration['additional-action-bar-templates']:
                self._action_bar_templates.append(ActionBarTemplate(template))

        self._image = ImageTk.PhotoImage(
            self._action_bar_templates[self._current_action_bar_template].image)
        super().__init__(root, image=self._image)

    def next_template(self):
        self._current_action_bar_template = self._current_action_bar_template
            + 1 % len(self._action_bar_templates)
        self._image = self._action_bar_templates[self._current_action_bar_template].image

class ActionBarTemplate:
    def __init__(self, template):
        self._file = template['file']
        self._num_rows = template['num-rows']
        self._num_columns = template['nums-columns']
        self._x_start = template['x-start']
        self._y_start = template['y-start']
        self._row_space = template['row-space']
        self._column_space = template['column-space']
        self._clickable_region_width = template['clickable-region-width']
        self._clickable_region_height = template['clickable-region-height']
        self._image = Image.open(self._file)

    @property
    def image(self):
        return self._image
