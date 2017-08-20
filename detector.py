#!/usr/bin/env python3
import cv2
import os
import os.path
from darkflow.net.build import TFNet

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
        return self.net.return_predict(cv2.imread(img_path))

    def detect_folder(self, img_folder):
        self.config['imgdir'] = os.path.abspath(img_folder)
        out_folder = os.path.join(self.config['imgdir'], 'out')
        if not os.path.isdir(out_folder):
            os.mkdir(out_folder)

        self.net = TFNet(self.config)
        self.net.predict()
        pass
