#!/usr/bin/env python3
from PIL import Image


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
        _label: The label for the box.
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
        self._label = label

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

    def label(self):
        return self._label

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

    def area(self):
        return self.w * self.h

    def __eq__(self, other):
        return (self.ulx == other.ulx) and (self.uly == other.uly) and (
            self.w == other.w) and (self.h == other.h)

    def __repr__(self):
        return 'Bounding Box(label: {l}, upper left: ({x}, {y}), width: {w}, height: {h})'.format(
            l=self._label, x=self.ulx, y=self.uly, w=self.w, h=self.h)

    def area_intersection(self, other):
        (x_min_1, y_min_1), (x_max_1,
                             y_max_1) = self.upper_left(), self.lower_right()
        (x_min_2, y_min_2), (
            x_max_2, y_max_2) = other.upper_left(), other.lower_right()
        x_len = min(x_max_1, x_max_2) - max(x_min_1, x_min_2)
        y_len = min(y_max_1, y_max_2) - max(y_min_1, y_min_2)

        if x_len < 0 or y_len < 0:
            return 0

        return x_len * y_len

    def area_union(self, other):
        return self.area() + other.area() - self.area_intersection(other)

    def iou(self, other):
        """Return the intersection over union
        """
        return self.area_intersection(other) / self.area_union(other)
