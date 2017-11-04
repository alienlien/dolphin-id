#!/usr/bin/env python3
# It is used to wrap an http server for the dolphin prediction.
import io
import json
import logging
import os.path
from tempfile import mkdtemp
from flask import redirect
from flask import request
from flask import Flask
from google.protobuf import json_format
from PIL import Image
import adapter as adp
from box import crop_image_for_box
from classifier import Classifier
from config import ConfigStore
from detector import FinDetector

# TODO: Centralize it into config.
DEFAULT_CFG_KEY = 'dolphin'

app = Flask(__name__)

fin_detector = FinDetector()
fin_classifier = Classifier(ConfigStore().get(DEFAULT_CFG_KEY))


@app.route('/prediction/image/', methods=['POST'])
def pred_image():
    if request.method != 'POST':
        return redirect(request.url)

    if 'file' not in request.files:
        logging.error('No file in request:', request.files)
        return redirect(request.url)

    req_file = request.files['file']
    if req_file.filename == '':
        logging.error('Filename is empty in request:', request.files)
        return redirect(request.url)

    temp_dir = mkdtemp()
    f_name = os.path.join(temp_dir, 'test.jpg')
    print('>> Temp image file:', f_name)

    data = io.BytesIO(req_file.read())
    img = Image.open(data)
    img.save(f_name)

    boxes = fin_detector.detect(f_name)
    box_imgs = [crop_image_for_box(f_name, box) for box in boxes]
    for idx, img in enumerate(box_imgs):
        boxes[idx].set_pred_labels(fin_classifier.predict(img))

    return json.dumps([
        json.loads(
            json_format.MessageToJson(
                adp.to_pb_region(box), including_default_value_fields=True))
        for box in boxes
    ])


@app.route('/prediction/image/fin/', methods=['POST'])
def pred_fin():
    if request.method != 'POST':
        return redirect(request.url)

    if 'file' not in request.files:
        logging.error('No file in request:', request.files)
        return redirect(request.url)

    req_file = request.files['file']
    if req_file.filename == '':
        logging.error('Filename is empty in request:', request.files)
        return redirect(request.url)

    temp_dir = mkdtemp()
    f_name = os.path.join(temp_dir, 'test.jpg')
    print('>> Temp image file:', f_name)

    data = io.BytesIO(req_file.read())
    img = Image.open(data)

    results = fin_classifier.predict(img)
    return json.dumps([
        json.loads(
            json_format.MessageToJson(
                adp.to_pb_prediction(x), including_default_value_fields=True))
        for x in results
    ])


if __name__ == '__main__':
    # Note that we disable the debug mode for flask here to resolve the issue
    # when a keras model runs on a flask app.
    # Ref: https://github.com/fchollet/keras/issues/2397
    app.run(debug=False)
