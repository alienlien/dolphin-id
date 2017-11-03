#!/usr/bin/env python3
# It is used to wrap an http server for the dolphin prediction.
import io
import json
import logging
import os.path
from tempfile import TemporaryFile, mkdtemp
from flask import redirect
from flask import request
from flask import Flask
from google.protobuf import json_format
from PIL import Image
from protobuf_to_dict import protobuf_to_dict
import adapter as adp
from box import ImageBoxes, crop_image_for_box, Box
from classifier import Classifier
from config import ConfigStore
from detector import FinDetector
import proto.image_pb2 as pb

# TODO: Centralize it into config.
DEFAULT_CFG_KEY = 'dolphin'

app = Flask(__name__)

fin_detector = FinDetector()
fin_classifier = Classifier(ConfigStore().get(DEFAULT_CFG_KEY))

# class ProtoJsonEncoder(json.JSONEncoder):
#
#     def default(self, obj):
#         if isinstance(obj, Box):
#             return obj.__dict__
#
#         return json.JSONEncoder.default(self, obj)
#
#     def default(self, obj):
#         print('>> Obj :', obj)
#         print('>> Dict:', obj.__dict__)
#         return obj.__dict__
#         if isinstance(obj, pb.Prediction):
#             return json_format.MessageToJson(obj)
#
#         return json.JSONEncoder.default(self, obj)


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

    # TODO: Resolve the issue about 'zero/default' value for protobuf.
    return json.dumps(
        [protobuf_to_dict(adp.to_pb_region(box)) for box in boxes])


#     return json.dumps(boxes, cls=ProtoJsonEncoder)

# @app.route('/prediction/image/fin/', methods=['POST'])
# def upload_file():
#     if request.method == 'POST':
#         print('>> Files:', request.files)
#         print('>> Headers:', request.headers)
#
#         if 'file' not in request.files:
#             logging.error('No file in request:', request.files)
#             return redirect(request.url)
#
#         req_file = request.files['file']
#         if req_file.filename == '':
#             logging.error('Filename is empty in request:', request.files)
#             return redirect(request.url)
#
#         data = io.BytesIO(req_file.read())
#         img = Image.open(data)
#         img.save('./test.png')
#
#         pred_1 = pb.Prediction()
#         pred_1.dolphin_id = 'ku_007'
#         pred_1.prob = 0.65
#
#         pred_2 = pb.Prediction()
#         pred_2.dolphin_id = '20170101_01'
#         pred_2.prob = 0.35
#
#     print('Type:', type(pred_1))
# #     return json_format.MessageToJson(pred_1)
#     test_data = {
#         'dolphinId': 'ku_007',
#         'prob': 0.65,
#     }
#     str_1 = json.dumps(json.dumps(test_data, indent=2))
#     str_2 = json_format.MessageToJson(pred_1)
#
#     pred_1_dict = json.loads(json_format.MessageToJson(pred_1))
#
#
#     print('>> Str1:', str_1)
#     print('>> [ENC] Proto:', ProtoJsonEncoder().encode(pred_1))
#     print('>> [ENC] Dict :', ProtoJsonEncoder().encode(test_data))
#     print('>> Dict:', json.dumps(test_data, indent=4))
#     print('>> One:', json.dumps(pred_1, cls=ProtoJsonEncoder))
#     print('>> Two:', json.dumps([pred_1, pred_2], cls=ProtoJsonEncoder))
#     print('>> Nested:', json.dumps(pred_1_dict))
#     print('>> ToDict:', json.dumps(protobuf_to_dict(pred_1)))
#     return json.dumps([protobuf_to_dict(pred_1), protobuf_to_dict(pred_2)])

# if __name__ == '__main__':
#     app.run(debug=True)
