from tracker.trackertools import TrackerTool, TrackerToolUI, TrackerToolConfiguration
import tkinter
import time

class APMCounter(TrackerTool):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.actions_time_queue = []
        self.sliding_time_window = self.configuration['apm-counter-sliding-time-window']
    
    def run(self, action_profile, action_map, actions, global_cooldown, player_state):
        current_time = time.time()
        for action in actions:
            self.actions_time_queue.append(current_time)
        while len(self.actions_time_queue) > 0:
            if current_time - self.actions_time_queue[0] > self.sliding_time_window:
                self.actions_time_queue.pop(0)
            else:
                break
        action_count = len(self.actions_time_queue)
        time_delta = self.actions_time_queue[-1] - self.actions_time_queue[0] if len(self.actions_time_queue) > 0 else self.sliding_time_window
        apm = (60 / self.sliding_time_window) * action_count * (time_delta / self.sliding_time_window)
        return([('apm-counter', int(apm))])

class APMCounterUI(TrackerToolUI):
    def __init__(self, configuration, root):
        super().__init__(configuration, root)
        self.widget = tkinter.Frame(root, background='black')
        self.apm = tkinter.StringVar()
        self.apm_text = configuration['apm-counter-text']
        self.apm.set(self.apm_text + '0')
        self.apm_widget = tkinter.Label(self.widget, anchor='center', textvariable=self.apm, font=('Arial', 16), fg='white', background='black')
        self.apm_widget.pack(side='left', fill='none', pady=4, padx=4)

    def draw(self, icon_map):
        if len(self.buffer) > 0:
            self.apm.set(self.apm_text + str(self.buffer[-1]))
            self.buffer = []
            
    @property
    def shape(self):
        return (20, 30)

class APMCounterConfiguration(TrackerToolConfiguration):
    def set_default_configuration(self):
        self.configuration['apm-counter-sliding-time-window'] = 15
