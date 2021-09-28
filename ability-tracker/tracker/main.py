import multiprocessing
from actiontracker import run_tracker, ActionTrackerUI


if __name__ == '__main__':
    ui_queue = multiprocessing.Queue()

    tracker_process = multiprocessing.Process(target=run_tracker, args=(ui_queue,))
    tracker_process.start()

    tracker_ui = ActionTrackerUI("ability-tracker\\icons\\",8, 25, (30,30), (4,4), ui_queue)
    tracker_ui.run()
