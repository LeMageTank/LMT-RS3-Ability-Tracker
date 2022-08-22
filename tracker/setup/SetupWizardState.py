from enum import Enum

class SetupWizardState(Enum):
    WELCOME_PAGE = 1
    ACKNOWLEDGE_PAGE = 2

    # Action bar setup
    ACTION_BAR_PRESET_SETUP_PAGE = 3
    ACTION_BAR_SETUP_PAGE = 4
    KEYBIND_SETUP_PAGE = 5

    # Static action sets
    STATIC_ACTION_SETS_PAGE = 6 # Use old action sets page
    STATIC_MOUSEBINDS_PAGE = 7 # Use old mousebinds page
    STATIC_KEYBINDS_PAGE = 8 # Use old keybinds page

    ACTION_BAR_AUTO_WEAPON_SWITCHES_PAGE = 10

    ACTION_BAR_BINDING_SETUP_PAGE = 11

    CONFIGURATION_ACTION_TRACKER_PAGE = 12
    CONFIGURATION_APM_COUNTER_PAGE = 13

    THEME_SETUP_PAGE = 14

    SETUP_COMPLETE_PAGE = 15
