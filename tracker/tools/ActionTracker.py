from tracker.TrackerExtension import TrackerExtensionController, TrackerExtensionUI, TrackerExtensionConfiguration
import tkinter
from PIL import Image

class ActionTracker(TrackerExtensionController):
    def run(self, action_map, actions, global_cooldown, player_state):
        output_list = []
        for action in actions:
            output_list.append(('action-tracker', action))
        return output_list

class ActionTrackerUI(TrackerExtensionUI):
    def __init__(self, configuration, root):
        super().__init__(configuration, root)
        self.max_icons = configuration['actiontracker-icons']
        self.icon_shape = configuration['actiontracker-icon-shape']
        self.padding = configuration['actiontracker-icon-padding']
        self.widget = tkinter.Frame(root, background='black')
        self.tracker_width = self.max_icons * (self.icon_shape[0] + self.padding[0])
        self.tracker_height = self.icon_shape[1] + self.padding[1]
        self.tracker_background_color = None if configuration['tracker-background-color'] == '' else configuration['tracker-background-color']
        self.action_bar_image_template = Image.new(mode='RGBA', size=(self.tracker_width, self.tracker_height), color=self.tracker_background_color)
        self.action_bar_image = self.action_bar_image_template.copy()
        self.action_bar_image_file_name = configuration['tracker-web-image-file']
        self.action_bar_image.save(self.action_bar_image_file_name, 'png')
        self.widget.configure(background=self.tracker_background_color)

    def draw(self, icon_map):
        if len(self.buffer) == 0:
            return
        for child in self.widget.winfo_children():
            child.destroy()
        while len(self.buffer) > 0:
            self.on_display.append(self.buffer.pop(0))
        while len(self.on_display) > self.max_icons:
            self.on_display.pop(0)
        new_action_bar_image = self.action_bar_image_template.copy()
        for i in range(len(self.on_display)-1, -1, -1):
            try:
                action_widget = tkinter.Label(self.widget, image=icon_map[self.on_display[i]], background=self.tracker_background_color)
                action_widget.pack(side='left', fill='none', pady=self.padding[1], padx=self.padding[0])
            except:
                action_widget = tkinter.Label(self.widget, text="?", background=self.tracker_background_color)
                action_widget.pack(side='left', fill='none', pady=self.padding[1], padx=self.padding[0])
            num_actions_on_display = len(self.on_display)
            position = num_actions_on_display - i - 1
            action_x1 = (position*(self.icon_shape[0] + self.padding[0]))
            action_x2 = action_x1 + icon_map[self.on_display[i]].width()
            action_y1 = self.padding[1]//2
            action_y2 = action_y1 + icon_map[self.on_display[i]].height()
            new_action_bar_image.paste(icon_map[self.on_display[i]].icon_image, box=(action_x1, action_y1, action_x2, action_y2))
        self.action_bar_image = new_action_bar_image
        self.action_bar_image.save(self.action_bar_image_file_name, 'png')
            
    @property
    def shape(self):
        return (((self.padding[0] * 2) + self.icon_shape[0]) * (self.max_icons + 1), (self.padding[1] * 3) + self.icon_shape[1])
        
class ActionTrackerConfiguration(TrackerExtensionConfiguration):
    def get_default_configuration(self):
        self.num_icons_var.set(8)
        return {'actiontracker-icons': 8,
        'actiontracker-icon-shape': [30,30],
        'actiontracker-icon-padding': [2,2]}

    def get_configuration_delta(self):
        return {'actiontracker-icons': self.num_icons_var.get()}

    def get_configuration_widget(self, root):
        widget = tkinter.Frame(root)
        num_icons_label = tkinter.Label(widget, text='No. Icons')
        num_icons_label.grid(row=0, column=0)
        self.num_icons_var = tkinter.IntVar()
        self.num_icons_var.set(8)
        self.num_icons_spinbox = tkinter.Spinbox(widget, from_=1, to=20, textvariable=self.num_icons_var)
        self.num_icons_spinbox.grid(row=0, column=1)
        return widget
        
    
