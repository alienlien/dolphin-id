#!/usr/bin/env python3
import json
import os.path
from PIL import Image

JSON_FILE = '/Users/Alien/workspace/project/private/dolphin-id/data/bounding-box/via_region_data-HL20100702_01.json'
IMAGES_ROOT = '/Users/Alien/workspace/project/private/dolphin-id/data/bounding-box/HL20100702_01'


class ImageBoxes(object):
    """
    Attributes:
        fname: File name of the image.
        data: Binary content of the image.
        boxes: All the bounding boxes.
    """

    def __init__(self, fname='', data=None, width=None, height=None, boxes=[]):
        self.fname = fname
        self.data = data
        self.w = width
        self.h = height
        self.boxes = boxes

    def width(self):
        if self.w:
            return self.w

        img = self.image()
        self.w, self.h = img.size
        return self.w

    def height(self):
        if self.h:
            return self.h

        img = self.image()
        self.w, self.h = img.size
        return self.h

    def image(self):
        if self.data:
            return self.data

        return Image.open(self.fname)

    def __eq__(self, other):
        return (self.fname == other.fname) and (self.boxes == other.boxes)

    def __repr__(self):
        return 'File: {f}, Width: {w}, Height: {h}, Boxes: {b}'.format(
            f=self.fname, w=self.width(), h=self.height(), b=self.boxes)


class Box():
    """
    Attributes:
        label: The label for the box.
        ulx, uly: Axis (x, y) for the upper left corner.
        w: Width of the box.
        h: Height of the box.
    """

    def __init__(self,
                 label,
                 upper_left=None,
                 lower_right=None,
                 center=None,
                 width=None,
                 height=None):
        self.label = label

        if upper_left and width and height:
            self.ulx = upper_left[0]
            self.uly = upper_left[1]
            self.w = width
            self.h = height
            return

        if center and width and height:
            self.ulx = center[0] - width / 2.0
            self.uly = center[1] - height / 2.0
            self.w = width
            self.h = height
            return

        if upper_left and lower_right:
            self.ulx = upper_left[0]
            self.uly = upper_left[1]
            self.w = lower_right[0] - upper_left[0]
            self.h = lower_right[1] - upper_left[1]

    def upper_left(self):
        return (self.ulx, self.uly)

    def lower_right(self):
        return (self.ulx + self.w, self.uly + self.h)

    def center(self):
        return (self.ulx + self.w / 2.0, self.uly + self.h / 2.0)

    def width(self):
        return self.w

    def height(self):
        return self.h

    def __eq__(self, other):
        return (self.ulx == other.ulx) and (self.uly == other.uly) and (
            self.w == other.w) and (self.h == other.h)

    def __repr__(self):
        return 'Bounding Box(label: {l}, upper left: ({x}, {y}), width: {w}, height: {h})'.format(
            l=self.label, x=self.ulx, y=self.uly, w=self.w, h=self.h)


def parse_via(root, imgs):
    """
    Args:
        root: Root for all the images.
        imgs: All the image data for the via bounding box file.
    """
    return [parse_via_image(root, img) for img in imgs.values()]


def parse_via_image(root, data):
    """
    Args:
        root: The root path for the image file.
        data: The meta data (including the boxes) of the image.

    {
        fileref: "",
        size: 2818332,
        filename: HL20100702_01_Gg_990702 (25).JPG,
        base64_img_data: "",
        file_attributes: {},
        regions: {
            0: {
                shape_attributes: {
                    name: rect,
                    x: 2208,
                    y: 1150,
                    width: 515,
                    height: 501
                },
                region_attributes: {}
            },
            1: {
                shape_attributes: {
                    name: rect,
                    x: 3643,
                    y: 221,
                    width: 236,
                    height: 192
                },
                region_attributes: {}
            }
        }
    }
    """
    fpath = os.path.join(root, data['filename'])
    boxes = [parse_via_box(k, v) for k, v in data['regions'].items()]
    return ImageBoxes(fname=fpath, boxes=boxes)


def parse_via_box(label, item):
    """
    {
        shape_attributes: {
            name: rect,
            x: 2208,
            y: 1150,
            width: 515,
            height: 501
        },
        region_attributes: {}
    }
    """
    content = item['shape_attributes']
    return Box(
        label=label,
        upper_left=(content['x'], content['y']),
        width=content['width'],
        height=content['height'])


def get_name(s):
    """It returns the real file name for the string in the json file.
    Example:
        Input : HL20100702_01_Gg_990702 (24).JPG2854363
        Return: HL20100702_01_Gg_990702 (24).JPG
    """
    basename = s.split('.JPG')[0]
    return basename + '.JPG'


if __name__ == '__main__':
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)

    print('Number of pics:', len(data))

    out = {}
    for item in data.values():
        n = len(item['regions'])
        if n not in out:
            out[n] = 0

        out[n] += 1

    print('Distribution for regions:', out)

    images = parse_via(IMAGES_ROOT, data)
    for img in images:
        print('>>', img)
