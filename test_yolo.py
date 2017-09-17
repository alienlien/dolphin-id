#!/usr/bin/env python3
import os.path
from pprint import pprint
import cv2
from darkflow.net.build import TFNet

IMAGE_FILE = os.path.abspath('./data/detector/src/HL20100730_02/HL20100730_02_Gg_047_IMG_8910.JPG')
IMAGE_FOLDER = os.path.abspath('/Users/Alien/workspace/project/private/dolphin-id/data/detector/test/image/')

options = {
    'model': 'config/tiny-yolo-dolphin.cfg',
    'load': -1,
    'threshold': 0.1,
    'labels': './labels_dolphin.txt',
    'imgdir': IMAGE_FOLDER,
    'json': False,
}

tfnet = TFNet(options)

result = tfnet.predict()
print('Result:', result)

# imgcv = cv2.imread(IMAGE_FILE)
# result = tfnet.return_predict(imgcv)
# pprint(result)
