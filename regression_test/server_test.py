#!/usr/bin/env python3
# Ref: https://docs.google.com/document/d/1PLFbp_0Rth4XpH3rHDPTQuE6hcUcJ9bNweMnH88FFwc/
from http import HTTPStatus
import json
import requests
from urllib.parse import urljoin
from google.protobuf import json_format
import sys
print('sys.path:', sys.path)
import proto.image_pb2 as pb
# from .. import proto.image_pb2 as pb
# import ..proto.image_pb2 as pb

API_URL = 'http://localhost:5000'
PRED_IMAGE_API = 'prediction/image/'
PRED_FIN_API = '/prediction/image/fin/'
# TEST_IMAGE = '/Users/Alien/workspace/project/private/dolphin-id/data/detector/validation/image/HL20100702_01_Gg_990702 (103)'
# TEST_IMAGE_FIN = '/Users/Alien/workspace/project/private/dolphin-id/data/classifier/src/20080713/01_Ku N000/st20080713_06_Gg_HY_ 228_a.JPG'
TEST_IMAGE = './test.jpg'


def assert_region(item):
    region = pb.Region()
    json_format.Parse(json.dumps(item), region)
    assert region.shape == pb.Region.RECTANGLE

def test_pred_image():
    url = urljoin(API_URL, PRED_IMAGE_API)
    files = {
        'file': open(TEST_IMAGE, 'rb'),
    }
    resp = requests.post(url, files=files)
    assert resp.status_code == HTTPStatus.OK

    results = json.loads(resp.text)
    assert isinstance(results, list)
    for item in results:
        assert_region(item)

def test_pred_fin():
    """It tests the fin prediction API.
    """
    url = urljoin(API_URL, PRED_FIN_API)
    files = {
        'file': open(TEST_IMAGE, 'rb'),
    }
    resp = requests.post(url, files=files)
    assert resp.status_code == HTTPStatus.OK

    result = json.loads(resp.text)
    assert isinstance(result, list)
    for item in result:
        assert len(item) == 2
        assert ('dolphinId' in item) and isinstance(item['dolphinId'], str)
        assert ('prob' in item) and isinstance(item['prob'],
                                               float) and item['prob'] >= 0.0
    sort_result = sorted(result, key=lambda x: x['prob'], reverse=True)
    assert result == sort_result
