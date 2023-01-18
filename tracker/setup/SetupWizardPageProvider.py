from tracker.setup.pages.WizardWelcomePage import WizardWelcomePage
from tracker.setup.pages.WizardAcknowledgePage import WizardAcknowledgePage
from tracker.setup.pages.WizardActionBarPresetSetupPage import WizardActionBarPresetSetupPage
from tracker.setup.pages.WizardActionBarSetupPage import WizardActionBarSetupPage
from tracker.setup.pages.WizardActionBarKeybindSetupPage import WizardActionBarKeybindSetupPage
from tracker.setup.pages.WizardActionBarMousebindSetupPage import WizardActionBarMousebindSetupPage
from tracker.setup.pages.WizardExtensionConfigurationPage import WizardExtensionConfigurationPage
from tracker.setup.pages.WizardWeaponSwitchSetupPage import WizardWeaponSwitchSetupPage
from tracker.setup.pages.WizardDefaultActionBarSetupPage import WizardDefaultActionBarSetupPage
from tracker.setup.pages.WizardSaveAndExitPage import WizardSaveAndExitPage
from tracker.setup.SetupWizardPageState import SetupWizardPageState


class SetupWizardPageProvider:
    def get_page_constructor(state):
        match state:
            case SetupWizardPageState.WELCOME_PAGE:
                return WizardWelcomePage
            case SetupWizardPageState.ACKNOWLEDGE_PAGE:
                return WizardAcknowledgePage
            case SetupWizardPageState.ACTION_BAR_PRESET_SETUP_PAGE:
                return WizardActionBarPresetSetupPage
            case SetupWizardPageState.ACTION_BAR_SETUP_PAGE:
                return WizardActionBarSetupPage
            case SetupWizardPageState.KEYBIND_SETUP_PAGE:
                return WizardActionBarKeybindSetupPage
            case SetupWizardPageState.MOUSEBIND_SETUP_PAGE:
                return WizardActionBarMousebindSetupPage
            case SetupWizardPageState.WEAPON_SWITCH_SETUP_PAGE:
                return WizardWeaponSwitchSetupPage
            case SetupWizardPageState.DEFAULT_ACTION_BAR_PRESET_SETUP_PAGE:
                return WizardDefaultActionBarSetupPage
            case SetupWizardPageState.SAVE_AND_EXIT_PAGE:
                return WizardSaveAndExitPage
            case default:
                raise Exception('Unknown page:' + state)
            
        
