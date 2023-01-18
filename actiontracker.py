import multiprocessing
import tracker.ActionTrackerUI
import json
import tkinter
from tracker.util.Configurator import load_configuration
from tracker.setup.SetupWizard import run_setup_wizard


if __name__ == '__main__':
    multiprocessing.freeze_support()
    configuration = load_configuration()
    #run_setup_wizard(configuration)
    tracker.ActionTrackerUI.run_tracker_ui(configuration)
    
 
