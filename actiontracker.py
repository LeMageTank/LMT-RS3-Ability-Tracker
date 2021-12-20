import multiprocessing
import tracker.actiontracker
import json
import tkinter

if __name__ == '__main__':
    multiprocessing.freeze_support()
    configuration = None
    with open('config.json', 'r+') as config_file:
        configuration = json.loads("".join(config_file.readlines()))
    tracker.actiontracker.run_tracker_ui(configuration)
