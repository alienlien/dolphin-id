#!/usr/bin/env python3
from docopt import docopt
from detector import FinDetector

usage = """
Usage:
    main.py [options]

Options:
    --type=TYPE     Type to predict. [default: single]
    --image=FILE    The image to predict. [default: ./data/detector/validation/image/HL20100702_01_Gg_990702 (26).JPG]
    --imgdir=DIR    The folder containing images to process.
"""

if __name__ == '__main__':
    args = docopt(usage, help=True)
    detector = FinDetector()

    print('Args:', args)

    if args['--type'].lower() == 'single':
        print(detector.detect(args['--image']))
