from tracker.trackertools import TrackerTool, TrackerToolUI, TrackerToolConfiguration
import tkinter

class ActionTracker(TrackerTool):
    def run(self, action_profile, action_map, actions, global_cooldown, player_state):
        output_list = []
        for action in actions:
            output_list.append(('action-tracker', action))
        return output_list

class ActionTrackerUI(TrackerToolUI):
    def __init__(self, configuration, root):
        super().__init__(configuration, root)
        self.max_icons = configuration['actiontracker-icons']
        self.icon_shape = configuration['actiontracker-icon-shape']
        self.padding = configuration['actiontracker-icon-padding']
        self.widget = tkinter.Frame(root, background='black')

    def draw(self, icon_map):
        if len(self.buffer) == 0:
            return
        for child in self.widget.winfo_children():
            child.destroy()
        while len(self.buffer) > 0:
            self.on_display.append(self.buffer.pop(0))
        while len(self.on_display) > self.max_icons:
            self.on_display.pop(0)
        for i in range(len(self.on_display)-1, -1, -1):
            try:
                action_widget = tkinter.Label(self.widget, image=icon_map[self.on_display[i]], background='black')
                action_widget.pack(side='left', fill='none', pady=self.padding[1], padx=self.padding[0])
            except:
                action_widget = tkinter.Label(self.widget, text="?", background='black')
                action_widget.pack(side='left', fill='none', pady=self.padding[1], padx=self.padding[0])
                
    @property
    def shape(self):
        return (((self.padding[0] * 2) + self.icon_shape[0]) * (self.max_icons + 1), (self.padding[1] * 3) + self.icon_shape[1])

class ActionTrackerConfiguration(TrackerToolConfiguration):
    def set_default_configuration(self):
        self.configuration['actiontracker-icons'] = 8
        self.configuration['actiontracker-icon-shape'] = [30,30]
        self.configuration['actiontracker-icon-padding'] = [2,2]
