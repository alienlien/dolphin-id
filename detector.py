#!/usr/bin/env python3
import json
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
        results = self.net.return_predict(cv2.imread(img_path))
        return [psr.from_flow_result(x) for x in results]

    def detect_folder(self, img_folder):
        """It returns the list of images with boxes detected.

        Args:
            img_folder: The folder containing image files to detect boxes.

        Returns:
            A map from the image file name to its boxes.
        """
        # Let the predictor returns the json output anyway.
        self.config['json'] = True

        img_folder = os.path.abspath(img_folder)
        self.config['imgdir'] = img_folder
        out_folder = os.path.join(img_folder, 'out')
        if not os.path.isdir(out_folder):
            os.mkdir(out_folder)

        self.net = TFNet(self.config)
        self.net.predict()

        json_files = [f for f in os.listdir(out_folder) if f.endswith('.json')]
        out = {}
        for fname in json_files:
            with open(os.path.join(out_folder, fname), 'r') as f:
                data = json.load(f)

            boxes = [psr.from_flow_result(x) for x in data]
            img_fname = os.path.join(img_folder, fname.replace(
                '.json', '.jpg'))
            out[img_fname] = boxes

        return out
