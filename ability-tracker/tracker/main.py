import multiprocessing
from actiontracker import run_tracker, TrackerUI
import json


if __name__ == '__main__':
    configuration = None
    with open('config.json', 'r+') as config_file:
        configuration = json.loads("".join(config_file.readlines()))
    
    manager_queue = multiprocessing.Queue()

    manager_process = multiprocessing.Process(target=run_tracker, args=(manager_queue, configuration))
    manager_process.start()

    tracker_ui = TrackerUI(configuration, manager_queue)
    tracker_ui.run()
