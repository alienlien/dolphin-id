#!/usr/bin/env python3
# It benchmarks the performances for the system.
import os
import os.path
import sys
from classifier import Classifier
from detector import FinDetector
from parser import xml_fname_from_jpg

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
            'image': os.path.join(IMG_FOLDER, img_file),
            'annotation': os.path.join(ANNO_FOLDER, anno_file),
        })

    for v in pairs:
        print('>> Pair:', v)
