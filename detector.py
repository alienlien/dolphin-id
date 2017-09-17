#!/usr/bin/env python3
import os
import os.path
import cv2
from darkflow.net.build import TFNet
import parser as psr

DEFAULT_CONFIG = {
    'model': 'config/tiny-yolo-dolphin.cfg',
    'load': -1,
    'threshold': 0.1,
    'labels': './labels_dolphin.txt',
    'json': False,
}


class FinDetector(object):
    """The fin detector.

    Attributes:
        config: The config to init the detector.
        net: The darkflow net to detect boxes.
    """

    def __init__(self, config=DEFAULT_CONFIG):
        self.config = config
        self.net = TFNet(self.config)

    def detect(self, img_path):
        """It returns the list of boxes detected.

        Args:
            img_path: The path of the image file.

        Returns:
            The list of boxes in the image.
        """
        print('File:', img_path)
        results = self.net.return_predict(cv2.imread(img_path))
        print('Results:', results)
        return [psr.from_flow_result(x) for x in results]

    def detect_folder(self, folder):
        """It returns the list of images with boxes detected.
        Note that we do not use the detect whole folder function for dark flow
        since we have to parse all the json files generated by dark flow
        and is really slower than one-by-one.

        Args:
            img_folder: The folder containing image files to detect boxes.

        Returns:
            A map from the image file name to its boxes.
        """

        file_list = [x for x in os.listdir(folder) if is_image(x)]
        file_list = [os.path.join(folder, x) for x in file_list]
        return {f: self.detect(f) for f in file_list}


def is_image(fname):
    """It checks whether the file fname is an image file or not.
    """
    return fname.lower().endswith('.jpg') or fname.lower().endswith('.jpeg')
