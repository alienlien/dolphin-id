#!/usr/bin/env python3
# This files is used to parse the boxes into the form darkflow needs.
import json
import os
import os.path
import sys
from box import Box, parse_via

IMAGE_FOLDER = '/Users/Alien/workspace/project/private/dolphin-id/data/bounding-box/HL20100702_01'


def gen_val(option, *args):
    """It returns the value based on the option and arguments input.
    """
    option = option.lower()

    if option == 'min':
        return min(*args)
    if option == 'max':
        return max(*args)
    return sum(args) / len(args)


def gen_square(box, option='avg'):
    """It returns a square box based on the box and the option input.
    Specifically, the box returns would have the same center as the box input,
    and the side length is determined according to the option input:
    min: The minimum of the width and height of the box input.
    avg: The average of the width and height of the box input.
    max: The maximum of the width and height of the box input.

    Args:
        box: The box input.
        option: The option for the side lenght of the square output.
    """
    side = gen_val(option, box.width(), box.height())
    return Box(label=box.label(), center=box.center(), width=side, height=side)


if __name__ == '__main__':
    file_list = os.listdir(IMAGE_FOLDER)
    box_files = [x for x in os.listdir(IMAGE_FOLDER) if x.endswith('json')]
    if len(box_files) == 0:
        print('No bounding box file in', IMAGE_FOLDER)
        sys.exit(0)

    if len(box_files) > 1:
        print('Too many bounding box files:', box_files)
        sys.exit(0)

    box_file = os.path.join(IMAGE_FOLDER, box_files[0])

    with open(box_file, 'r') as f:
        data = json.load(f)

    imgs = parse_via(IMAGE_FOLDER, data)
    for img in imgs:
        img.boxes = [gen_square(box, option='max') for box in img.boxes]

    for item in imgs:
        print('>>', item)
