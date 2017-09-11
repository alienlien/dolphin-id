#!/usr/bin/env python3
# This file is used to prepare the data set needed for the training
# of the fin detector.
# Source:
# <src_folder>/img_1.jpg, img_2.jpg, ..., img_N.jpg,
#                /all_the_boxes(annotations).json
#
# Result:
# <training folder>/image/img_t1.jpg, img_t2.jpg, ..., img_tn.jpg
#                  /annotation/img_t1.xml, img_t2.xml, ..., img_tn.xml
# <validation folder>/image/img_v1.jpg, img_v2.jpg, ..., img_vm.jpg
#                    /annotation/img_v1.xml, img_v2.xml, ..., img_vm.xml
import os
import os.path
import shutil
from parser import VIAParser, gen_xml_string, xml_fname_from_jpg
from split import split_files

SOURCE_FOLDER = './data/detector/src/HL20100823_04_gg_fix'
TRAIN_FOLDER = './data/detector/test_id/train/'
VALIDATION_FOLDER = './data/detector/test_id/validation/'
VAL_RATIO = 0.2
IS_SHUFFLE = True


def gen_image_folder(root):
    return os.path.join(root, './image')


def gen_anno_folder(root):
    return os.path.join(root, './annotation')


def get_json(src_folder, tp='fin'):
    """It returns the json file from source folder.

    Args:
        src_folder: The folder containing the json file.

    Returns:
        The json file containing all the information about bounding boxes.
    """
    if tp == 'id':
        is_box_file = is_id_box_file
    else:
        is_box_file = is_old_style_box_file

    box_files = [x for x in os.listdir(src_folder) if is_box_file(x)]
    print('>> Candidates of box files:', box_files)
    if len(box_files) == 0:
        print('No bounding box file in', src_folder)
        return ''

    if len(box_files) > 1:
        print('Too many bounding box files:', box_files)
        return ''

    return os.path.join(src_folder, box_files[0])


def is_old_style_box_file(json_fname):
    """Note that we use '_2.json' to identify that
    it is the json file containing box information and the boxes
    are followed old style, the rectangle not the square ones.
    """
    return json_fname.endswith('_2.json')


def is_id_box_file(json_fname):
    """It checks whether the json file input contains labels
    (i.e., group/ku id) or not.
    """
    # TODO: Determine the naming rules for (via) box files.
    return json_fname.endswith('_ID.json') or json_fname.endswith('_ID2.json')


def parse_source_folder(parser, json_file, img_folder):
    """It parses the via json file and returns all the images with boxes,
    where the filename in the image objects are all of the full path
    containing the img_folder.
    """
    imgs = parser.parse(json_file)

    for k, img in imgs.items():
        imgs[k].fname = os.path.join(img_folder, img.fname)

    return imgs


def gen_image_folders(src_folder):
    """It returns the list of all the image sub folders
    in the source folder src_folder.
    """
    out = []
    for root, dirs, files in os.walk(src_folder):
        img_files = [x for x in files if x.lower().endswith('.jpg')]
        if img_files and not dirs:
            out.append(root)
    return out


def gen_folders(train_folder, valid_folder):
    return {
        'train': {
            'image': gen_image_folder(train_folder),
            'anno': gen_anno_folder(train_folder),
        },
        'validation': {
            'image': gen_image_folder(valid_folder),
            'anno': gen_anno_folder(valid_folder),
        },
    }


if __name__ == '__main__':
    # TODO: Add config store.
    src_folder = os.path.abspath(SOURCE_FOLDER)
    train_folder = os.path.abspath(TRAIN_FOLDER)
    valid_folder = os.path.abspath(VALIDATION_FOLDER)

    for fdr in [train_folder, valid_folder]:
        if not os.path.isdir(fdr):
            os.mkdir(fdr)

    folders = gen_folders(train_folder, valid_folder)
    img_folders = gen_image_folders(src_folder)

    for fdrs in folders.values():
        for fdr in fdrs.values():
            if not os.path.isdir(fdr):
                os.mkdir(fdr)

    parser = VIAParser()
    imgs = {}
    for folder in img_folders:
        print('>> Processing Image Folder:', folder)
        imgs.update(
            parse_source_folder(parser, get_json(folder, 'id'), folder))

    result = split_files(list(imgs.keys()), VAL_RATIO, IS_SHUFFLE)

    for tp in ['train', 'validation']:
        print('>> Begin to copy image files for:', tp)
        for k in result[tp]:
            shutil.copy(imgs[k].fname, folders[tp]['image'])

        print('>> Begin to generate xml files for:', tp)
        for k in result[tp]:
            xml_fname = xml_fname_from_jpg(imgs[k].fname)
            dst = os.path.join(folders[tp]['anno'], xml_fname)
            with open(dst, 'w') as f:
                f.write(gen_xml_string(imgs[k]))
