import multiprocessing
import tracker.ActionTrackerUI
import json
import tkinter
from tracker.util.Configurator import load_configuration

if __name__ == '__main__':
    multiprocessing.freeze_support()
    configuration = None
    configuration = load_configuration()
    tracker.ActionTrackerUI.run_tracker_ui(configuration)
