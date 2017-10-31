#!/usr/bin/env python3
# This files is used to parse the boxes into the form darkflow needs.
import json
import os
import os.path
import re
import sys
from xml.etree import ElementTree as et
from xml.dom.minidom import parseString
from box import Box, ImageBoxes
from split import copy_files_to_folder

SRC_FOLDER = './data/detector/src/test'
IMAGE_FOLDER = './data/detector/train/image'
ANNO_FOLDER = './data/detector/train/annotation'
FIN_LABEL = 'fin'
GROUP_ID_KEY_1 = 'GROUP ID'
GROUP_ID_KEY_2 = 'GROUP_ID'
KU_ID_KEY_1 = 'KU ID'
KU_ID_KEY_2 = 'KU_ID'


class VIAParser(object):
    """It is the parser for the vgg via json file.
    """

    def __init__(self):
        pass

    def parse(self, json_file):
        with open(json_file, 'r') as f:
            return parse_via_json(f)


def parse_via_json(f):
    """
    Args:
        f: The file descriptor of the json file.
    """
    data = json.load(f)
    return {k: parse_via_image(img) for k, img in data.items()}


def parse_via_image(data):
    """
    Args:
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
                "region_attributes": {
                    "GROUP ID": "01",
                    "KU ID": "085"
                }
            }
        }
    }
    """
    prefix = prefix_for_filename(data['filename'])
    boxes = [parse_via_box(v, prefix) for v in data['regions'].values()]
    boxes = [x for x in boxes if x.is_valid()]
    return ImageBoxes(fname=data['filename'], boxes=boxes)


def prefix_for_filename(fname):
    """It returns the prefix for the group id from file name input.
    Note that we now use the file name directly rather than the folder.
    One day we might need to fetch the 'Date' information (i.e., prefix)
    from folder import directly.

    Args:
        fname: File name of the image.

    Return:
        The prefix used for the group id of that file.

    Example:
        Input : HL20100702_01_Gg_990702 (25).JPG
        Return: 20100702
    """
    group_name = fname.split('_')[0]
    return re.findall('\d+', group_name)[0]


def parse_via_box(item, prefix=''):
    """
    {
        shape_attributes: {
            name: rect,
            x: 2208,
            y: 1150,
            width: 515,
            height: 501
        },
        "region_attributes": {
            "GROUP ID": "01",
            "KU ID": "085"
        }
    }
    """
    content = item['shape_attributes']
    ids = item['region_attributes']
    label = FIN_LABEL
    if ids:
        group_id = ids.get(GROUP_ID_KEY_1, '') or ids.get(GROUP_ID_KEY_2, '')
        ku_id = ids.get(KU_ID_KEY_1, '') or ids.get(KU_ID_KEY_2, '')
        label = label_for(ku_id, group_id, prefix)
    return Box(
        label=label,
        upper_left=(content['x'], content['y']),
        width=content['width'],
        height=content['height'])


def label_for(ku_id, group_id, prefix_gid):
    if ku_id:
        return ku_id_for(ku_id)
    if group_id:
        return group_id_for(prefix_gid, group_id)
    # Default value if there are no ku id and group id.
    return FIN_LABEL


def ku_id_for(kid):
    """It returns the ku ID for id input.

    Args:
        kid: ku id in the format of number string only (e.g., '00034')
    """
    return 'ku_{0:03d}'.format(int(kid))


def group_id_for(prefix, gid):
    """It returns the group id for the prefix and id input.

    Args:
        prefix: The prefix for the group id output.
        gid: The group id input (e.g., '007')
    """
    return '{0}_{1:02d}'.format(prefix, int(gid))


def gen_xml_string(img_box):
    """It generates the corresbonding xml string for the image input
    It follows the XML format of VOC 2007 such that the classifier can
    read the box data.

    # FIXME. I CANNOT go to the web for voc. FXXK.
    Ref: http://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/index.html
         8.3 Submission of Results
    """
    return xml_nodes_to_string(gen_xml_nodes(img_box))


def gen_xml_nodes(img_box):
    """
    <?xml version="1.0" ?>
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
    root = et.Element('annotation')
    node_fname = et.SubElement(root, 'filename')
    node_fname.text = img_box.fname

    node_size = et.SubElement(root, 'size')
    width = et.SubElement(node_size, 'width')
    width.text = str(img_box.width())
    height = et.SubElement(node_size, 'height')
    height.text = str(img_box.height())
    depth = et.SubElement(node_size, 'depth')
    depth.text = '3'

    for box in img_box.boxes:
        node_obj = et.SubElement(root, 'object')
        label = et.SubElement(node_obj, 'name')
        label.text = str(box.label())
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


def from_xml(f):
    """It parses the xml file descriptor and returns an image object.

    Args:
        f: The file object for the xml file.

    Return:
        An image object that containing all the info in the xml.
    """
    root = et.parse(f).getroot()

    fname = root.find('filename').text

    size = root.find('size')
    width = size.find('width')
    height = size.find('height')

    boxes = []
    for box in root.findall('object'):
        label = box.find('name').text
        bndbox = box.find('bndbox')
        upper_left = (float(bndbox.find('xmin').text),
                      float(bndbox.find('ymin').text))
        lower_right = (float(bndbox.find('xmax').text),
                       float(bndbox.find('ymax').text))
        boxes.append(
            Box(label=label, upper_left=upper_left, lower_right=lower_right))
    return ImageBoxes(fname=fname, width=width, height=height, boxes=boxes)


def xml_fname_from_jpg(s):
    """It returns the corresponding xml file from jpg file with path s.
    """
    return os.path.basename(s).replace('.JPG', '.xml').replace('.jpg', '.xml')


def from_flow_result(item):
    """It returns the box from result generated from darkflow.
        {
            'label': 'fin',
            'topleft': {
                'x': 2578,
                'y': 533,
            },
            'bottomright': {
                'x': 2959,
                'y': 978,
            },
            'confidence': 0.45233271,
        }
    """
    return Box(
        label=item['label'],
        upper_left=(item['topleft']['x'], item['topleft']['y']),
        lower_right=(item['bottomright']['x'], item['bottomright']['y']),
        confidence=float(item['confidence']), )


if __name__ == '__main__':
    """It parses the via boxes file input and generate the corresponding
    annotation files of xml format used in VOC 2007.
    """
    parser = VIAParser()
    src_folder = os.path.abspath(SRC_FOLDER)
    image_folder = os.path.abspath(IMAGE_FOLDER)
    anno_folder = os.path.abspath(ANNO_FOLDER)

    file_list = os.listdir(src_folder)
    box_files = [x for x in os.listdir(src_folder) if x.endswith('json')]
    if len(box_files) == 0:
        print('No bounding box file in', src_folder)
        sys.exit(0)

    if len(box_files) > 1:
        print('Too many bounding box files:', box_files)
        sys.exit(0)

    box_file = os.path.join(src_folder, box_files[0])
    imgs = parser.parse(box_file)

    for k, img in imgs.items():
        imgs[k].fname = os.path.join(src_folder, img.fname)

    img_files = [x.fname for x in imgs.values()]
    copy_files_to_folder(img_files, image_folder)

    for img in imgs.values():
        xml_str = gen_xml_string(img)
        fpath = os.path.join(anno_folder, xml_fname_from_jpg(img.fname))
        with open(fpath, 'w') as f:
            f.write(xml_str)
