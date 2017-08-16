#!/usr/bin/env python3
import json
import parser as p
# from parser import squarize, gen_val
from box import Box, ImageBoxes

test_label = 'test_label'
test_center = (128.0, 27.0)
test_width = 81.0
test_height = 24.0
test_label_2 = 'test_222'
test_center_2 = (289, 137)
test_width_2 = 45
test_height_2 = 42
test_file_name = 'aaabbb.jpg'
test_image_width = 1024
test_image_height = 768
test_image_boxes = ImageBoxes(
    fname=test_file_name,
    width=test_image_width,
    height=test_image_height,
    boxes=[
        Box(
            label=test_label,
            center=test_center,
            width=test_width,
            height=test_height, ), Box(
                label=test_label_2,
                center=test_center_2,
                width=test_width_2,
                height=test_height_2, )
    ])


def test_parse_via_image():
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
    actual = p.parse_via_image(data)
    expected = ImageBoxes(
        fname='HL20100702_01_Gg_990702 (26).JPG',
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


def test_gen_xml_string():
    actual = p.gen_xml_string(test_image_boxes)
    expected = """<?xml version="1.0" ?>
<annotation>
    <filename>aaabbb.jpg</filename>
    <size>
        <width>1024</width>
        <height>768</height>
        <depth>3</depth>
    </size>
    <object>
        <name>test_label</name>
        <bndbox>
            <xmin>87.5</xmin>
            <ymin>15.0</ymin>
            <xmax>168.5</xmax>
            <ymax>39.0</ymax>
        </bndbox>
    </object>
    <object>
        <name>test_222</name>
        <bndbox>
            <xmin>266.5</xmin>
            <ymin>116.0</ymin>
            <xmax>311.5</xmax>
            <ymax>158.0</ymax>
        </bndbox>
    </object>
</annotation>
"""
    assert actual == expected


def test_xml_fname_from_jpg():
    s = './aaa/bbb/ccc/ddd.jpg'
    assert p.xml_fname_from_jpg(s) == 'ddd.xml'

    s = '/aaa/bbb/ccc/xyz.JPG'
    assert p.xml_fname_from_jpg(s) == 'xyz.xml'


# def test_gen_yolo_box():
#     box = Box(
#         label=test_label,
#         center=(100, 201),
#         width=70,
#         height=252, )
#     actual = p.gen_yolo_box(400, 600, box)
#     expected = test_label, 0.25, 0.335, 0.175, 0.42
#     assert actual == expected
