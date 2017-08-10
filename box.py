#!/usr/bin/env python3
import json

JSON_FILE = '/Users/Alien/workspace/project/private/dolphin-id/data/HL20100702_01/via_region_data HL20100702_01.json'


class Image(object):
    """
    Attributes:
        fname: File name of the image.
        data: Binary content of the image.
        boxes: All the bounding boxes.
    """

    def __init__(self, fname, data, width, height, boxes=[]):

        if fname:
            self.fname = fname

        if data:
            self.data = data

        if width:
            self.width = width

        if height:
            self.height = height

        self.boxes = boxes


class Box():
    """
    Attributes:

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
