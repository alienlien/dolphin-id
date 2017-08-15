#!/usr/bin/env python3
import os.path
import cv2
from darkflow.net.build import TFNet

IMAGE_FILE = os.path.abspath('./data/bounding-box/train/image/HL20100730_02_Gg_064_IMG_8928.JPG')
print('>> Image file to process:', IMAGE_FILE)

options = {
    'model': 'config/tiny-yolo-dolphin.cfg',
    'load': -1,
    'threshold': 0.1,
    'labels': './labels_dolphin.txt',
}

tfnet = TFNet(options)

imgcv = cv2.imread(IMAGE_FILE)
result = tfnet.return_predict(imgcv)
print(result)
