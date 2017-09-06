#!/usr/bin/env python3
# TODO: Rewrite it as a flask app if needed.
import sys
from docopt import docopt
from detector import FinDetector
from classifier import Classifier
from box import ImageBoxes, crop_image_for_box

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
        box_imgs = [crop_image_for_box(box) for box in boxes]
        for idx, img in enumerate(box_imgs):
            boxes[idx].set_pred_labels(classifier.predict(img))
        img = ImageBoxes(fname=img_path, boxes=boxes)

        print('Image:', img)

    if tp.lower() == 'multi':
        print('>> Ready to parse image folder:', img_folder)
        result = detector.detect_folder(img_folder)
        images = []
        for fname, boxes in result.items():
            box_imgs = [crop_image_for_box(fname, box) for box in boxes]
            for idx, box_img in enumerate(box_imgs):
                boxes[idx].set_pred_labels(classifier.predict(box_img))
            img = ImageBoxes(fname=fname, boxes=boxes)
            print('>> Image:', img)
            print('-----------------------------------------')
            images.append(img)
