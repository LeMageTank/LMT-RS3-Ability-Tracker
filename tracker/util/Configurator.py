import json
from filelock import FileLock

def load_configuration():
    with open('config.json', 'r+') as config_file:
        return json.loads(''.join(config_file.readlines()))

def save_configuration(configuration):
    with open('config.json', 'w') as config_file:
        config_file.write(json.dumps(configuration, indent=4))

def save_configuration_options(delta_map):
    with FileLock('config.json.lock'):
        config = load_configuration()
        for key, value in delta_map.items():
            config[key] = value
        save_configuration(config)
