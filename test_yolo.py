#!/usr/bin/env python3
# It is used to test the fin detector.
# Note that when testing the detection of a whole folder, one needs to
# add a sub-folder 'out' for the images with bounding box generated.
import os.path
from pprint import pprint
import cv2
from darkflow.net.build import TFNet
from docopt import docopt

options = {
    'model': 'config/tiny-yolo-dolphin.cfg',
    'load': -1,
    'threshold': 0.1,
    'labels': './labels_dolphin.txt',
    'json': False,
}

usage = """
Usage:
    ./test_yolo.py [options]

Options:
    --img=FILE      The image file to test.
    --imgdir=DIR    The image folder to test.
"""
if __name__ == '__main__':
    args = docopt(usage, help=True)

    if args['--img']:
        tfnet = TFNet(options)
        imgcv = cv2.imread(os.path.abspath(args['--img']))
        result = tfnet.return_predict(imgcv)
        pprint(result)

    if args['--imgdir']:
        options['imgdir'] = os.path.abspath(args['--imgdir'])
        tfnet = TFNet(options)
        tfnet.predict()
