#!/usr/bin/env python3
# TODO: Rewrite it as a flask app if needed.
import sys
from docopt import docopt
from detector import FinDetector
from classifier import Classifier
from box import ImageBoxes

usage = """
Usage:
    main.py [options]

Options:
    --type=TYPE     Type to predict. [default: single]
    --image=FILE    The image to predict.
    --imgdir=DIR    The folder containing images to process.
"""

if __name__ == '__main__':
    args = docopt(usage, help=True)
    tp = args['--type']
    img_path = args['--image']
    img_folder = args['--imgdir']

    # Check the parameters first since it cost lots of time to init...
    if tp.lower() == 'single' and not img_path:
        print('>> Should provide image path for type:', tp)
        sys.exit(0)

    if tp.lower() == 'multi' and not img_folder:
        print('>> Should provide image folder for type:', tp)
        sys.exit(0)

    print('>> Initialize fin detector...')
    detector = FinDetector()
    print('>> Initialize Risso\'s dolphin classifier...')
    classifier = Classifier()

    if tp.lower() == 'single':
        boxes = detector.detect(img_path)
        img = ImageBoxes(fname=img_path, boxes=boxes)
        print('Image:', img)
        for img in img.box_images():
            print(classifier.predict(img))

    if tp.lower() == 'multi':
        print('>> Ready to parse image folder:', img_folder)
        result = detector.detect_folder(img_folder)
        images = [
            ImageBoxes(fname=fname, boxes=bxs)
            for fname, bxs in result.items()
        ]

        for img in images:
            print(img)
            for box_img in img.box_images():
                print(classifier.predict(box_img))
            print('-----------------------------------')
