#!/usr/bin/env python3
# It benchmarks the performances for the system.
import os
import os.path
import sys
from box import ImageBoxes
from box import crop_image_for_box
from classifier import Classifier
from detector import FinDetector
from parser import xml_fname_from_jpg, from_xml

IMG_FOLDER = os.path.abspath('./data/detector/test/image/')
ANNO_FOLDER = os.path.abspath('./data/detector/test/annotation/')
IOU_THRESHOLD = 0.5

if __name__ == '__main__':
    classifier = Classifier()
    detector = FinDetector()

    img_files = [x for x in os.listdir(IMG_FOLDER)]
    anno_files = {x: True for x in os.listdir(ANNO_FOLDER)}

    if len(img_files) != len(anno_files):
        print('No match for image and annotation files.')
        sys.exit(0)

    # Pairs is the list of all the images and their corresponding annotations.
    pairs = []
    for img_file in img_files:
        anno_file = xml_fname_from_jpg(img_file)
        if anno_file not in anno_files:
            print('Image {f} is has no annotation:'.format(f=img_file))
            sys.exit(0)

        pairs.append({
            'files': {
                'image': os.path.join(IMG_FOLDER, img_file),
                'annotation': os.path.join(ANNO_FOLDER, anno_file),
            },
        })

    for idx, pair in enumerate(pairs):
        with open(pair['files']['annotation'], 'r') as f:
            pairs[idx]['answers'] = from_xml(f)

    for idx, pair in enumerate(pairs):
        img_file = pair['files']['image']
        # TODO: combine detect + classify as a function?
        boxes = detector.detect(img_file)
        box_imgs = [crop_image_for_box(img_file, box) for box in boxes]
        for j, img in enumerate(box_imgs):
            boxes[j].set_pred_labels(classifier.predict(img))
        img = ImageBoxes(fname=img_file, boxes=boxes)

        pairs[idx]['prediction'] = img

    for pair in pairs:
        print('>> Pair:', pair)
        print('-----------------------------------------')
