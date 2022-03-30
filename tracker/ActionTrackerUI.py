from pynput import mouse, keyboard
import multiprocessing
import subprocess
import os
import json
import math
import time
import tkinter
import pyautogui
from PIL import Image, ImageDraw, ImageTk
import numpy as np
from tracker.actions.Action import Action
from tracker.actions.KeybindAction import KeybindAction
from tracker.actions.ActionProfile import ActionProfile
from tracker.profilecreator import run_profilecreator
from tracker.ui.TrackerUITool import TrackerUITool
from tracker.ActionTrackerController import run_tracker_controller
from tracker.util.Configurator import load_configuration, save_configuration_options
import importlib


class ActionTrackerUI:
    def __init__(self, configuration):
        self._configuration = configuration
        self._root = tkinter.Tk()
        self._icon_map = self.load_icons(configuration['action-icon-directory'])
        self._icon_history = []
        self._max_icons = configuration['actiontracker-icons']
        self._update_interval = configuration['actiontracker-update-interval']
        self._icon_shape = configuration['actiontracker-icon-shape']
        self._padding = configuration['actiontracker-icon-padding']
        self._input_queue = multiprocessing.Queue()
        self._controller_queue = multiprocessing.Queue()
        self._root.title("LMT's Ability Tracker")
        self._root.overrideredirect(True)
        self._root.attributes('-topmost', configuration['actiontracker-always-on-top'])
        self._root.configure(background='black')
        self._paused = False
        self._controls_container = tkinter.Frame(self._root)
        self.load_controls(self._controls_container)
        self.load_tools()        
        self._controls_container.grid(row=0, column=0, sticky=tkinter.W)
        self._width = 90
        self._height = 18
        self._root.geometry("{}x{}+{}+{}".format(self._width, self._height, configuration['tracker-window-position'][0], configuration['tracker-window-position'][1]))
        self.start_tracker()

    def start_tracker(self):
        self.tracker_process = multiprocessing.Process(target=run_tracker_controller,
                                                       args=(self._input_queue, self._controller_queue, self._configuration))
        self.tracker_process.start()

    def close(self):
        configuration_delta = {}
        configuration_delta['tracker-window-position'] = [self._root.winfo_x(), self._root.winfo_y()]
        
        for key, tool_queue in self._uitracker_tools.items():
            tool_queue.put(('control_event', 'exit'))

        any_extensions_open = True
        while False:
            any_extensions_open = False
            for process in self._uitracker_tool_processes:
                if process.is_alive():
                    any_extensions_open = True
        self._input_queue.put('exit')
        save_configuration_options(configuration_delta)
        self._root.destroy()
        
    def move_window(self, event):
        x,y = self._root.winfo_pointerxy()
        self._root.geometry("{}x{}+{}+{}".format(self._width, self._height, x, y))

    def load_controls(self, controls_container):
        self._play_button_image = ImageTk.PhotoImage(Image.open(self._configuration['play-image-file']).resize((12,12)))
        self._pause_button_image = ImageTk.PhotoImage(Image.open(self._configuration['pause-image-file']).resize((12,12)))
        self._refresh_button_image = ImageTk.PhotoImage(Image.open(self._configuration['refresh-image-file']).resize((12,12)))
        self._configuration_button_image = ImageTk.PhotoImage(Image.open(self._configuration['configuration-image-file']).resize((12,12)))
        self._move_button_image = ImageTk.PhotoImage(Image.open(self._configuration['move-image-file']).resize((12,12)))
        self._exit_button_image = ImageTk.PhotoImage(Image.open(self._configuration['exit-image-file']).resize((12,12)))
        self._play_pause_button = tkinter.Button(controls_container, image=self._play_button_image,
                                                 command=self.play_pause_button_event, height=12, width=12)
        self._refresh_button = tkinter.Button(controls_container, image=self._refresh_button_image,
                                                 command=self.refresh_button_event, height=12, width=12)
        self._configuration_button = tkinter.Button(controls_container, image=self._configuration_button_image,
                                                 command=self.configuration_button_event, height=12, width=12)
        self._move_button = tkinter.Button(controls_container, image=self._move_button_image, height=12, width=12)
        self._exit_button = tkinter.Button(controls_container, image=self._exit_button_image,
                                                 command= lambda: self.close(), height=12, width=12)

        self._move_button.bind('<B1-Motion>', self.move_window)
        self._move_button.grid(row=0, column=0, sticky=tkinter.W)
        self._play_pause_button.grid(row=0, column=1, sticky=tkinter.W)
        self._refresh_button.grid(row=0, column=2, sticky=tkinter.W)
        self._configuration_button.grid(row=0, column=3, sticky=tkinter.W)
        self._exit_button.grid(row=0, column=4, sticky=tkinter.W)

    def play_pause_button_event(self):
        if self._paused:
            self._play_pause_button.configure(image=self._play_button_image)
            self._input_queue.put('play')    
        else:
            self._play_pause_button.configure(image=self._pause_button_image)
            self._input_queue.put('pause')
        self._paused = not self._paused

    def configuration_button_event(self):
        self._input_queue.put('configuration-open')
        self._paused = True
        self._play_pause_button.configure(image=self._pause_button_image)
        self._input_queue.put('pause')

    def refresh_button_event(self):
        self._input_queue.put('refresh')

    def load_tools(self):
        num_tools = 0
        tools = {}
        tool_processes = []
        for tool in self._configuration['tools']:
            if tool['enabled']:
                tool_ui_control_queue = multiprocessing.Queue()
                tool_ui_process = multiprocessing.Process(target=run_tracker_ui_tool,
                                                          args=(tool_ui_control_queue, tool, self._configuration))
                tool_ui_process.start()
                tool_processes.append(tool_ui_process)
                tools[tool['name']] = tool_ui_control_queue
        self._uitracker_tools = tools
        self._uitracker_tool_processes = tool_processes

    def load_icons(self, path):
        icon_map = {}
        for file in os.listdir(path):
            icon = tkinter.PhotoImage(file=(path + file))
            icon_map[file.split('.')[0]] = icon
        return icon_map

    def update(self):
        while self._controller_queue.qsize() > 0:
            item = self._controller_queue.get()
            self._uitracker_tools[item[0]].put(('tracker_event',item[1]))
        self._root.after(self._update_interval, self.update)

    def run(self):
        self.update()
        self._root.mainloop()
        

def run_tracker_ui_tool(control_queue, tool_config, configuration):
    try:
        tool_ui = TrackerUITool(configuration, control_queue, tool_config)
        tool_ui.start()
    except Exception as e:
        open(configuration['logs-directory'] + '-{}-exception.log'.format(tool_config['name']), 'w+').write('Exception: ' + str(e))

def run_tracker_ui(configuration):
    multiprocessing.freeze_support()
    tracker_ui = ActionTrackerUI(configuration)
    tracker_ui.run()
