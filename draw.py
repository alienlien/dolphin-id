#!/usr/bin/env python3
# It is used to draw the boxes on the pic.
# import os.path
# import sys
from docopt import docopt
from PIL import Image, ImageDraw
from parser import from_xml

DEFAULT_WIDTH = 20  # Width for the boxes.

usage = """
Usage:
    draw.py [options]

Options:
    --img=FILE  The file to draw.
    --anno=FILE The annotation file (.xml)
"""
if __name__ == '__main__':
    args = docopt(usage, help=True)

    with open(args['--anno'], 'r') as f:
        boxes = from_xml(f).boxes

    img = Image.open(args['--img'])
    draw = ImageDraw.Draw(img)

    for box in boxes:
        (ulx, uly), (lrx, lry) = box.upper_left(), box.lower_right()
        width = DEFAULT_WIDTH
        for shift in range(0, width):
            draw.rectangle(
                [(ulx + shift, uly + shift), (lrx + shift, lry + shift)],
                outline='yellow')

    img.save('./output.png', 'PNG')
