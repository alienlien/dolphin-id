#!/usr/bin/env python3
import os.path
import cv2
from darkflow.net.build import TFNet

IMAGE_FILE = os.path.abspath('./data/detector/train/image/HL20100730_02_Gg_064_IMG_8928.JPG')
IMAGE_FOLDER = os.path.abspath('/Users/Alien/workspace/project/private/dolphin-id/data/detector/src/HL20120708_01_gg_fix')

options = {
    'model': 'config/tiny-yolo-dolphin.cfg',
    'load': -1,
    'threshold': 0.1,
    'labels': './labels_dolphin.txt',
    'imgdir': IMAGE_FOLDER,
    'json': True,
}

tfnet = TFNet(options)

tfnet.predict()

# imgcv = cv2.imread(IMAGE_FILE)
# result = tfnet.return_predict(imgcv)
# print(result)
