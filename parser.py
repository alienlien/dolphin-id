#!/usr/bin/env python3
# This files is used to parse the boxes into the form darkflow needs.
import json
import os
import os.path
import sys
from xml.etree import ElementTree as et
from xml.dom.minidom import parseString
from box import Box, ImageBoxes

IMAGE_FOLDER = '/Users/Alien/workspace/project/private/dolphin-id/data/bounding-box/HL20100702_01'
FIN_LABEL = 0


def parse_via(root, imgs):
    """
    Args:
        root: Root for all the images.
        imgs: All the image data for the via bounding box file.
    """
    return [parse_via_image(root, img) for img in imgs.values()]


def parse_via_image(root, data):
    """
    Args:
        root: The root path for the image file.
        data: The meta data (including the boxes) of the image.

    {
        fileref: "",
        size: 2818332,
        filename: HL20100702_01_Gg_990702 (25).JPG,
        base64_img_data: "",
        file_attributes: {},
        regions: {
            0: {
                shape_attributes: {
                    name: rect,
                    x: 2208,
                    y: 1150,
                    width: 515,
                    height: 501
                },
                region_attributes: {}
            },
            1: {
                shape_attributes: {
                    name: rect,
                    x: 3643,
                    y: 221,
                    width: 236,
                    height: 192
                },
                region_attributes: {}
            }
        }
    }
    """
    fpath = os.path.join(root, data['filename'])
    boxes = [parse_via_box(FIN_LABEL, v) for v in data['regions'].values()]
    return ImageBoxes(fname=fpath, boxes=boxes)


def parse_via_box(label, item):
    """
    {
        shape_attributes: {
            name: rect,
            x: 2208,
            y: 1150,
            width: 515,
            height: 501
        },
        region_attributes: {}
    }
    """
    content = item['shape_attributes']
    return Box(
        label=label,
        upper_left=(content['x'], content['y']),
        width=content['width'],
        height=content['height'])


def gen_val(option, *args):
    """It returns the value based on the option and arguments input.
    """
    option = option.lower()

    if option == 'min':
        return min(*args)
    if option == 'max':
        return max(*args)
    return sum(args) / len(args)


def gen_square(box, option='avg'):
    """It returns a square box based on the box and the option input.
    Specifically, the box returns would have the same center as the box input,
    and the side length is determined according to the option input:
    min: The minimum of the width and height of the box input.
    avg: The average of the width and height of the box input.
    max: The maximum of the width and height of the box input.

    Args:
        box: The box input.
        option: The option for the side lenght of the square output.
    """
    side = gen_val(option, box.width(), box.height())
    return Box(label=box.label(), center=box.center(), width=side, height=side)


# def gen_yolo_box(img_width, img_height, box):
#     """
#     Args:
#         img_width: The width of the image the box belongs to.
#         img_height: The height of the image the box belongs to.
#         box: The box input.
#
#     Returns:
#         label, cx, cy, width, height
#         Note that the center axis (cx, cy), width and height are normalized.
#
#     Ref:
#         https://timebutt.github.io/static/how-to-train-yolov2-to-detect-custom-objects/
#     """
#     (cx, cy) = box.center()
#     return box.label(), \
#         cx / img_width, \
#         cy / img_height, \
#         box.width() / img_width, \
#         box.height() / img_height


def gen_xml_string(img_box):
    return xml_nodes_to_string(gen_xml_nodes(img_box))


def gen_xml_nodes(img_box):
    root = et.Element('annotation')
    node_fname = et.SubElement(root, 'filename')
    node_fname.text = img_box.fname

    node_size = et.SubElement(root, 'size')
    width = et.SubElement(node_size, 'width')
    width.text = img_box.width().__repr__()
    height = et.SubElement(node_size, 'height')
    height.text = img_box.height().__repr__()
    depth = et.SubElement(node_size, 'depth')
    depth.text = '3'

    for box in img_box.boxes:
        node_obj = et.SubElement(root, 'object')
        label = et.SubElement(node_obj, 'name')
        label.text = box.label()
        node_box = et.SubElement(node_obj, 'bndbox')
        (ulx, uly) = box.upper_left()
        xmin = et.SubElement(node_box, 'xmin')
        xmin.text = str(ulx)
        ymin = et.SubElement(node_box, 'ymin')
        ymin.text = str(uly)
        (lrx, lry) = box.lower_right()
        xmax = et.SubElement(node_box, 'xmax')
        xmax.text = str(lrx)
        ymax = et.SubElement(node_box, 'ymax')
        ymax.text = str(lry)
    return root


def xml_nodes_to_string(nodes):
    return parseString(et.tostring(nodes)).toprettyxml(indent='    ')


if __name__ == '__main__':
    file_list = os.listdir(IMAGE_FOLDER)
    box_files = [x for x in os.listdir(IMAGE_FOLDER) if x.endswith('json')]
    if len(box_files) == 0:
        print('No bounding box file in', IMAGE_FOLDER)
        sys.exit(0)

    if len(box_files) > 1:
        print('Too many bounding box files:', box_files)
        sys.exit(0)

    box_file = os.path.join(IMAGE_FOLDER, box_files[0])

    with open(box_file, 'r') as f:
        data = json.load(f)

    imgs = parse_via(IMAGE_FOLDER, data)
    for img in imgs:
        img.boxes = [gen_square(box, option='max') for box in img.boxes]

    for item in imgs:
        print('>>', item)
