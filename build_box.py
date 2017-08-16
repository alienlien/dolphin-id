#!/usr/bin/env python3
# This file is used to build the data set needed for the training
# of the fin detector.
# Source:
# <source_folder>/img_1.jpg, img_2.jpg, ..., img_N.jpg,
#                /all_the_boxes(annotations).json
#
# Result:
# <training folder>/image/img_t1.jpg, img_t2.jpg, ..., img_tn.jpg
#                  /annotation/img_t1.xml, img_t2.xml, ..., img_tn.xml
# <validation folder>/image/img_v1.jpg, img_v2.jpg, ..., img_vm.jpg
#                    /annotation/img_v1.xml, img_v2.xml, ..., img_vm.xml
import os
import os.path
import sys
from parser import VIAParser, gen_square

SOURCE_FOLDER = './data/bounding-box/src/HL20100803_01_gg_fix/'
TRAIN_FOLDER = './data/bounding-box/train/'
VALIDATION_FOLDER = './data/bounding-box/validation/'


def get_json(src_folder):
    """It returns the json file from source folder.

    Args:
        src_folder: The folder containing the json file.

    Returns:
        The json file containing all the information about bounding boxes.
    """

    box_files = [x for x in os.listdir(src_folder) if x.endswith('json')]
    if len(box_files) == 0:
        print('No bounding box file in', src_folder)
        return ''

    if len(box_files) > 1:
        print('Too many bounding box files:', box_files)
        return ''

    return os.path.join(src_folder, box_files[0])


if __name__ == '__main__':
    json_file = get_json(SOURCE_FOLDER)

    if not json_file:
        sys.exit(0)

    parser = VIAParser()
    imgs = parser.parse(json_file)

    for k, img in imgs.items():
        imgs[k].fname = os.path.join(SOURCE_FOLDER, img.fname)
        imgs[k].boxes = [gen_square(box, option='max') for box in img.boxes]
