from enum import Enum, auto

class SetupWizardPageState(Enum):
    WELCOME_PAGE = auto()
    ACKNOWLEDGE_PAGE = auto()
    ACTION_BAR_PRESET_SETUP_PAGE = auto()
    ACTION_BAR_SETUP_PAGE = auto()
    KEYBIND_SETUP_PAGE = auto()
    MOUSEBIND_SETUP_PAGE = auto()
    WEAPON_SWITCH_SETUP_PAGE = auto()
    DEFAULT_ACTION_BAR_PRESET_SETUP_PAGE = auto()
    ACTION_BAR_BINDING_SETUP_PAGE = auto() # TODO
    CONFIGURE_EXTENSIONS_PAGE = auto() # TODO
    SAVE_AND_EXIT_PAGE = auto()
