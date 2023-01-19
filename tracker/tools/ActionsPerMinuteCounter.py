from tracker.TrackerExtension import TrackerExtensionController, TrackerExtensionUI, TrackerExtensionConfiguration
import tkinter
import time

class APMCounter(TrackerExtensionController):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.actions_time_queue = []
        self.sliding_time_window = self.configuration['apm-counter-sliding-time-window']
    
    def run(self, action_map, actions, global_cooldown, player_state):
        current_time = time.time()
        for action in actions:
            self.actions_time_queue.append(current_time)
        while len(self.actions_time_queue) > 0:
            if current_time - self.actions_time_queue[0] > self.sliding_time_window:
                self.actions_time_queue.pop(0)
            else:
                break
        action_count = len(self.actions_time_queue)
        time_delta = self.actions_time_queue[-1] - self.actions_time_queue[0] if len(self.actions_time_queue) > 1 else self.sliding_time_window
        apm = (60 / time_delta) * action_count
        return([('apm-counter', int(apm))])

class APMCounterUI(TrackerExtensionUI):
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
        width = (len(self.apm_text) + 3) * 14
        return (width, 30)

class APMCounterConfiguration(TrackerExtensionConfiguration):
    def get_default_configuration(self):
        self.apm_text_var.set('APM: ')
        self.window_time_var.set(30.0)
        return {'apm-counter-sliding-time-window': 30.0,
                'apm-counter-text': 'APM: ' }

    def get_configuration_delta(self):
        apm_text = self.apm_text_var.get()
        window_time = self.window_time_var.get()
        return {'apm-counter-sliding-time-window': window_time,
                'apm-counter-text': apm_text }

    def get_configuration_widget(self, root):
        widget = tkinter.Frame(root)
        apm_text_label = tkinter.Label(widget, text='Output prefix')
        apm_text_label.grid(row=0, column=0)
        self.apm_text_var = tkinter.StringVar()
        self.apm_text_var.set(self.configuration['apm-counter-text'])
        self.apm_text_entry = tkinter.Entry(widget, textvariable = self.apm_text_var)
        self.apm_text_entry.grid(row=0, column=1)
        window_time_text_label = tkinter.Label(widget, text='Time Tracking Length (seconds)')
        window_time_text_label.grid(row=1, column=0)
        self.window_time_var = tkinter.DoubleVar()
        self.window_time_var.set(self.configuration['apm-counter-sliding-time-window'])
        self.window_time_scale = tkinter.Scale(widget, variable=self.window_time_var,
                                               from_=5.4, to=180, orient=tkinter.HORIZONTAL)
        self.window_time_scale.grid(row=1, column=1)
        return widget        
