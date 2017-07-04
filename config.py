#!/usr/bin/env python3
import os
import os.path
import sys
import json
from docopt import docopt

DEFAULT_CONFIG_FILE = './config.json'


class ConfigStore:
    """Storage for configs.
       Note that we con't consider the multi-thread problem here.
    """

    def __init__(self, config_file=DEFAULT_CONFIG_FILE):
        if not os.path.exists(config_file):
            with open(config_file, 'w') as f:
                json.dump({}, f)

        self.config_file = config_file

    def get(self, key):
        with open(self.config_file, 'r') as f:
            configs = json.load(f)

        if key not in configs:
            return {}

        return configs[key]

    def set(self, config):
        with open(self.config_file, 'r') as f:
            configs = json.load(f)

        configs[config['name']] = config
        with open(self.config_file, 'w') as f:
            json.dump(configs, f, indent=2)


def get_labels(data_dir):
    return sorted(list(os.walk(data_dir))[0][1])


def get_key(data_dir):
    return os.path.basename(os.path.abspath(data_dir))


def get_name(data_dir):
    return os.path.basename(os.path.abspath(data_dir))


def get_model(data_dir):
    return './model/inception-{k}.h5'.format(k=get_key(data_dir))


usage = """
Usage:
    config.py [options]

Options:
    --data_dir=DIR  The directory contains data. [default: ./data/20110607]
    --name=STR      The name of the config.
    --model=FILE    The model file.

"""
if __name__ == '__main__':
    args = docopt(usage, help=True)
    data_dir, name, model = args['--data_dir'], args['--name'], args['--model']

    if not data_dir:
        print('One should provide data dir.')
        sys.exit(0)

    if not name:
        name = get_name(data_dir)

    if not model:
        model = get_model(data_dir)

    config = {
        'name': name,
        'data_dir': data_dir,
        'model': model,
        'labels': get_labels(data_dir),
    }

    config_store = ConfigStore()
    config_store.set(config)
    print(config_store.get(name))
