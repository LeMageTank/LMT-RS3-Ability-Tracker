import multiprocessing
import tracker.ActionTrackerUI
import json
import tkinter
from tracker.util.Configurator import Configurator
from tracker.setup.SetupWizard import run_setup_wizard


if __name__ == '__main__':
    multiprocessing.freeze_support()
    configuration = Configurator.load_configuration()
    if not configuration['user-has-completed-setup']:
        run_setup_wizard(configuration)
    tracker.ActionTrackerUI.run_tracker_ui(configuration)
    

