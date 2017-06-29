#!/usr/bin/env python3
import os
import os.path
import sys
import json
from docopt import docopt


def get_labels(data_dir):
    return list(os.walk(data_dir))[0][1]


def get_name(data_dir):
    return os.path.basename(os.path.abspath(data_dir))


def gen_config(data_dir):
    return {
        'name': get_name(data_dir),
        'labels': get_labels(data_dir),
    }


usage = """
Usage:
    config.py [options]

Options:
    --data_dir=DIR      The directory contains data. [default: ./data/20110607]
    --config_file=FILE  The config file. [default: config.json]
"""
if __name__ == '__main__':
    args = docopt(usage, help=True)
    data_dir, config_file = args['--data_dir'], args['--config_file']

    configs = {}
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            configs = json.load(f)

    config = gen_config(data_dir)
    if config['name'] in configs:
        sys.exit(0)

    configs[config['name']] = config
    with open(config_file, 'w') as f:
        json.dump(configs, f, indent=2, ensure_ascii=False)
