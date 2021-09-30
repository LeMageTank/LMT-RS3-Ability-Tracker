import multiprocessing
from actiontracker import run_tracker, ActionTrackerUI
import json


if __name__ == '__main__':
    configuration = None
    with open('config.json', 'r+') as config_file:
        configuration = json.loads("".join(config_file.readlines()))
    
    ui_queue = multiprocessing.Queue()

    tracker_process = multiprocessing.Process(target=run_tracker, args=(ui_queue, configuration))
    tracker_process.start()

    tracker_ui = ActionTrackerUI(configuration, ui_queue)
    tracker_ui.run()
