import json
from filelock import FileLock


class Configurator:
    configuration = None

    @staticmethod
    def load_configuration():
        with open('config.json', 'r+') as config_file:
            Configurator.configuration = json.loads(''.join(config_file.readlines()))
            return Configurator.configuration

    @staticmethod
    def save_configuration():
        with open('config.json', 'w') as config_file:
            config_file.write(json.dumps(Configurator.configuration, indent=4))

    @staticmethod
    def save_configuration_options(delta_map):
        with FileLock('config.json.lock'):
            if Configurator.configuration is None:
                Configurator.load_configuration()
            for key, value in delta_map.items():
                Configurator.configuration[key] = value
            Configurator.save_configuration()
