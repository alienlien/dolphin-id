#!/usr/bin/env python3
# TODO: Resolve not json serializable problem. Might replace it with proto.
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
        self._box_images = []

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

    def box_images(self):
        """It returns the images in its boxes.
        """
        if self._box_images:
            return self._box_images

        imgs = [crop_image_for_box(self.fname, box) for box in self.boxes]
        self._box_images = imgs
        return imgs

    def __eq__(self, other):
        return (self.fname == other.fname) and (self.boxes == other.boxes)

    def __repr__(self):
        return 'File: {f}, Width: {w}, Height: {h}, Boxes: {b}'.format(
            f=self.fname, w=self.width(), h=self.height(), b=self.boxes)


def crop_image_for_box(img_path, box):
    """It crops the image content for the box from image img_path.

    Args:
        img_path: The path of the image file.
        box: The box to crop.

    Return:
        The PIL image object cropped from image.
    """
    img = Image.open(img_path)
    (ulx, uly), (lrx, lry) = box.upper_left(), box.lower_right()
    return img.crop((ulx, uly, lrx, lry))


class Box():
    """
    Attributes:
        _label: The label for the box.
        ulx, uly: Axis (x, y) for the upper left corner.
        w: Width of the box.
        h: Height of the box.
        _confidence: Confidence about the box.
        _pred_labels: Labels predicted with their corresponding prob.
                      [
                        {'label': 'aaa', 'prob': 0.9},
                        {'label': 'bbb', 'prob': 0.7},
                        ...
                      ]
    """

    def __init__(self,
                 label='',
                 upper_left=None,
                 lower_right=None,
                 center=None,
                 width=None,
                 height=None,
                 confidence=0.0,
                 pred_labels=None):

        self._label = label
        self._confidence = confidence

        # Init the prediction labels.
        # Note that we sort the ranked labels according to their probabilities.
        if pred_labels and isinstance(pred_labels, list):
            self._pred_labels = get_sorted_pred_labels(pred_labels)
        else:
            self._pred_labels = []

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
            return

        # If no valid init, returns an empty box.
        self.label = ''
        self.ulx = self.uly = self.w = self.h = 0

    def label(self):
        return self._label

    def set_label(self, label):
        self._label = label

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

    def confidence(self):
        return self._confidence

    def pred_labels(self):
        return self._pred_labels

    def set_pred_labels(self, pred_labels):
        self._pred_labels = get_sorted_pred_labels(pred_labels)

    def area(self):
        return self.w * self.h

    def is_valid(self):
        return self.w and self.h

    def __eq__(self, other):
        return (self.ulx == other.ulx) and (self.uly == other.uly) and (
            self.w == other.w) and (self.h == other.h)

    def __repr__(self):
        return 'Bounding Box(label: {l}, upper left: ({x}, {y}), width: {w}, height: {h}, confidence: {c}, pred labels: {p})'.format(
            l=self._label,
            x=self.ulx,
            y=self.uly,
            w=self.w,
            h=self.h,
            c=self._confidence,
            p=self._pred_labels)

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


def get_sorted_pred_labels(pred_labels):
    """It returns the sorted prediction label list.
    """
    return sorted(pred_labels, key=lambda x: x.get('prob', 0.0), reverse=True)
