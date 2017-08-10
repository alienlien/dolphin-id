#!/usr/bin/env python3
import json
from box import Image, Box, parse_via_image

test_label = 'test'
test_upper_left = (13.0, 17.0)
test_lower_right = (42.0, 53.0)
test_center = (27.5, 35.0)
test_width = 29.0
test_height = 36.0


def assert_box(b):
    assert b.upper_left() == test_upper_left
    assert b.lower_right() == test_lower_right
    assert b.center() == test_center
    assert b.width() == test_width
    assert b.height() == test_height


def test_box_init_1():
    b = Box(
        label=test_label,
        upper_left=test_upper_left,
        lower_right=test_lower_right)
    assert_box(b)


def test_box_init_2():
    b = Box(
        label=test_label,
        center=test_center,
        width=test_width,
        height=test_height)
    assert_box(b)


def test_box_init_3():
    b = Box(
        label=test_label,
        upper_left=test_upper_left,
        lower_right=test_lower_right)
    assert_box(b)


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
    actual = parse_via_image(root, data)
    expected = Image(
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
