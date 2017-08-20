#!/usr/bin/env python3
import cv2
import os
import os.path
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
        results = self.net.return_predict(cv2.imread(img_path))
        return [
            psr.gen_square(psr.from_flow_result(x), 'max') for x in results
        ]

    def detect_folder(self, img_folder):
        img_folder = os.path.abspath(img_folder)
        self.config['imgdir'] = img_folder
        out_folder = os.path.join(img_folder, 'out')
        if not os.path.isdir(out_folder):
            os.mkdir(out_folder)

        self.net = TFNet(self.config)
        self.net.predict()
