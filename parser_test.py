#!/usr/bin/env python3
import json
import parser as p
# from parser import squarize, gen_val
from box import Box, ImageBoxes

test_label = 'test_label'
test_center = (128.0, 27.0)
test_width = 81.0
test_height = 24.0


def test_parse_via_image():
    root = 'aaa/bbb/ccc'
    img_json_str = '''{
        "fileref": "",
        "size": 2785695,
        "filename": "HL20100702_01_Gg_990702 (26).JPG",
        "base64_img_data": "",
        "file_attributes": {},
        "regions": {
            "0": {
                "shape_attributes": {
                    "name": "rect",
                    "x": 1596,
                    "y": 944,
                    "width": 524,
                    "height": 460
                },
                "region_attributes": {}
            },
            "1": {
                "shape_attributes": {
                    "name": "rect",
                    "x": 3052,
                    "y": 175,
                    "width": 341,
                    "height": 306
                },
                "region_attributes": {}
            }
        }
    }'''
    data = json.loads(img_json_str)
    actual = p.parse_via_image(root, data)
    expected = ImageBoxes(
        fname='aaa/bbb/ccc/HL20100702_01_Gg_990702 (26).JPG',
        boxes=[
            Box(
                label=0,
                upper_left=(1596, 944),
                width=524,
                height=460, ),
            Box(
                label=1,
                upper_left=(3052, 175),
                width=341,
                height=306, ),
        ])
    assert actual == expected


def test_gen_val():
    assert p.gen_val('MIN', 19.0, 11.0, 33.0) == 11.0
    assert p.gen_val('Max', 19.0, 11.0, 33.0) == 33.0
    assert p.gen_val('average', 19.0, 11.0, 33.0) == 21.0


def test_gen_square():
    box = Box(
        label=test_label,
        center=test_center,
        width=test_width,
        height=test_height, )

    actual = p.gen_square(box, option='avg')
    expected = Box(
        label=test_label,
        center=test_center,
        width=52.5,
        height=52.5, )
    assert actual == expected


def test_gen_yolo_box():
    box = Box(
        label=test_label,
        center=(100, 201),
        width=70,
        height=252, )
    actual = p.gen_yolo_box(400, 600, box)
    expected = test_label, 0.25, 0.335, 0.175, 0.42
    assert actual == expected
