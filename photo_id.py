#!/usr/bin/env python3
# This file is used to generate photo id.
# That is, it would cut the fin images according their corresponding
# bounding boxes and copies them to corresponding folders.
# TODO: Unify all the util function when preparing data, such as
#       getting id files, copying files, and others.
# TODO: Add scripts or sop to get data for fin detector.
import os
import os.path
# from PIL import Image
from box import crop_image_for_box
from parser import VIAParser
from prepare_detector import get_json, gen_image_folders, parse_source_folder

SRC_FOLDER = './data/detector/src/HL20100702_01/'
DST_FOLDER = './data/test_dst/'

if __name__ == '__main__':
    parser = VIAParser()

    src_folder = os.path.abspath(SRC_FOLDER)
    dst_folder = os.path.abspath(DST_FOLDER)
    img_folders = gen_image_folders(src_folder)

    for idx, folder in enumerate(img_folders):
        print('Index: {0:4d}, Folder: {1}'.format(idx, folder))

    imgs = {}
    for folder in img_folders:
        print('>> Processing Image Folder:', folder)

        box_id_file = get_json(folder, 'id')
        if not box_id_file:
            print('The image folder has no id file:', folder)
            continue

        imgs.update(parse_source_folder(parser, box_id_file, folder))

    num_img = len(imgs)
    num_boxes = sum([len(img.boxes) for img in imgs.values()])

    print('Total number of images: {}, boxes: {}'.format(num_img, num_boxes))

    counter = 0

    for img in imgs.values():
        if counter % 10 == 0:
            print('>> Processing {0:4d}th / {1} images.'.format(
                counter, num_img))
        counter += 1

        fname = img.fname

        if not os.path.isfile(fname):
            print('There is no corresponding file for json:', fname)
            continue

        box_fname_base = os.path.basename(fname).split('.')[0].replace(
            ' ', '_').replace('(', '').replace(')', '')
        for idx, box in enumerate(img.boxes):
            box_img = crop_image_for_box(fname, box)
            box_fname = '{base}_{idx}.jpg'.format(base=box_fname_base, idx=idx)

            dst_dir = os.path.join(dst_folder, box.label())
            if not os.path.isdir(dst_dir):
                os.mkdir(dst_dir)
            box_img.save(os.path.join(dst_dir, box_fname))
