#!/usr/bin/env python3
# Ref: https://docs.google.com/document/d/1PLFbp_0Rth4XpH3rHDPTQuE6hcUcJ9bNweMnH88FFwc/
import json
import requests
from urllib.parse import urljoin
from google.protobuf import json_format
# Note that the importing only works when
# 1) pytest in the source dir (repo root)
# 2) ./test.sh: Set the environ var PYTHONPATH as repo root.
# Ref: https://stackoverflow.com/questions/25827160/importing-correctly-with-pytest
import proto.image_pb2 as pb

API_URL = 'http://localhost:5000'
PRED_IMAGE_API = 'prediction/image/'
PRED_FIN_API = '/prediction/image/fin/'
TEST_IMAGE = './image.jpg'
TEST_IMAGE_FIN = './fin.jpg'


def assert_region(item):
    region = pb.Region()
    json_format.Parse(json.dumps(item), region)
    assert region.shape == pb.Region.RECTANGLE


# It tests the following image prediction API.
# Request:
# curl -X POST \
#   -H "X-Application-Id: ${APPLICATION_ID}" \
#   -H "X-REST-API-Key: ${REST_API_KEY}" \
#   -F "file=@${file path}" \
#   http://${server url:port}/prediction/image/
#
# Response:
# [					// List of regions in the image
#   {
#     "shape": enum (RECTANGLE),	// Region shape. Json format: string.
#     "rectangleProperty": {		// Property of a rectangle.
#       "upperLeftX": float,		// X-axis of the upper left corner.
#       "upperLeftY": float,		// Y-axis of the upper left corner.
#       "width": float,			// Width of the rectangle.
#       "height": float			// Height of the rectangle.
#     },
#     "dolphinId": string,		// Dolphin ID.
#     "groupId": int,			// ID w.r.t. that sighting.
#     "predictions": [			// List of dolphin ID predicted.
#       {
#         "dolphinId": string,	        // Dolphin ID.
#         "prob": float			// Probability of the prediction.
#       },
#       ...
#     ]
#   },
#   ...
# ]
def test_pred_image():
    url = urljoin(API_URL, PRED_IMAGE_API)
    files = {
        'file': open(TEST_IMAGE, 'rb'),
    }
    resp = requests.post(url, files=files)
    assert resp.status_code == 200

    results = json.loads(resp.text)
    assert isinstance(results, list)
    for item in results:
        assert_region(item)


# It tests the following fin prediction API.
# Request:
# curl -X POST \
#   -H "X-Application-Id: ${APPLICATION_ID}" \
#   -H "X-REST-API-Key: ${REST_API_KEY}" \
#   -F "file=@${file path}" \
#   http://${server url:port}/prediction/image/fin/
#
# Response:
# [				// List of dolphin ID predicted.
#   {
#     "dolphinId": string,	// Dolphin ID.
#     "prob": float		// Probability of the prediction.
#   },
#   ...
# ]
def test_pred_fin():
    """It tests the fin prediction API.
    """
    url = urljoin(API_URL, PRED_FIN_API)
    files = {
        'file': open(TEST_IMAGE_FIN, 'rb'),
    }
    resp = requests.post(url, files=files)
    assert resp.status_code == 200

    result = json.loads(resp.text)
    assert isinstance(result, list)
    for item in result:
        assert len(item) == 2
        assert ('dolphinId' in item) and isinstance(item['dolphinId'], str)
        assert ('prob' in item) and isinstance(item['prob'],
                                               float) and item['prob'] >= 0.0
    sort_result = sorted(result, key=lambda x: x['prob'], reverse=True)
    assert result == sort_result
