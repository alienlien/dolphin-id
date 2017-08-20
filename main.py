#!/usr/bin/env python3
from docopt import docopt
from PIL import Image
from detector import FinDetector
from classifier import Classifier

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
    tp = args['--type']
    detector = FinDetector()
    classifier = Classifier()

    if tp.lower() == 'single':
        img_path = args['--image']
        boxes = detector.detect(img_path)
        print('>> Fin boxes:', boxes)

        img_src = Image.open(img_path)
        for box in boxes:
            (ulx, uly), (lrx, lry) = box.upper_left(), box.lower_right()
            img_fin = img_src.crop((ulx, uly, lrx, lry))
            print(classifier.predict(img_fin))
