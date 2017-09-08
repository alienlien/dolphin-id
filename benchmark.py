#!/usr/bin/env python3
# It benchmarks the performances for the system.
import os
import os.path
import sys
from box import ImageBoxes
from box import crop_image_for_box
from classifier import Classifier
from detector import FinDetector
from parser import xml_fname_from_jpg, from_xml
from precision import is_overlap, get_num_hit_rank

IMG_FOLDER = os.path.abspath('./data/detector/test_id/train/image/')
ANNO_FOLDER = os.path.abspath('./data/detector/test_id/train/annotation/')
IOU_THRESHOLD = 0.5

if __name__ == '__main__':
    classifier = Classifier()
    detector = FinDetector()

    img_files = [x for x in os.listdir(IMG_FOLDER)]
    anno_files = {x: True for x in os.listdir(ANNO_FOLDER)}

    if len(img_files) != len(anno_files):
        print('No match for image and annotation files.')
        sys.exit(0)

    # data is the list of all the images and their corresponding annotations.
    data = []
    for img_file in img_files:
        anno_file = xml_fname_from_jpg(img_file)
        if anno_file not in anno_files:
            print('Image {f} is has no annotation:'.format(f=img_file))
            sys.exit(0)

        data.append({
            'files': {
                'image': os.path.join(IMG_FOLDER, img_file),
                'annotation': os.path.join(ANNO_FOLDER, anno_file),
            },
        })

    for idx, datum in enumerate(data):
        with open(datum['files']['annotation'], 'r') as f:
            data[idx]['truth'] = from_xml(f)

    for idx, datum in enumerate(data):
        img_file = datum['files']['image']
        # TODO: combine detect + classify as a function?
        boxes = detector.detect(img_file)
        box_imgs = [crop_image_for_box(img_file, box) for box in boxes]
        for j, img in enumerate(box_imgs):
            boxes[j].set_pred_labels(classifier.predict(img))
        img = ImageBoxes(fname=img_file, boxes=boxes)

        data[idx]['prediction'] = img

    print('>> Number of boxes predicted:',
          sum([len(x['prediction'].boxes) for x in data]))

    # Keep only the boxes in prediction if it overlaps some box in ground truth
    for idx, datum in enumerate(data):
        boxes_truth = datum['truth'].boxes
        boxes_pred = datum['prediction'].boxes

        boxes_overlap = []
        for pbox in datum['prediction'].boxes:
            for tbox in datum['truth'].boxes:
                if is_overlap(pbox, tbox, IOU_THRESHOLD):
                    boxes_overlap.append(pbox)
                    break
        data[idx]['prediction'].boxes = boxes_overlap

    print('>> Number of boxes predicted [Overlapped with ground truth]:',
          sum([len(x['prediction'].boxes) for x in data]))

    num_rel = sum([len(x['truth'].boxes) for x in data])
    num_det, num_hit = 0, 0
    # TODO: Add config for the max. of rank.
    for rank in range(0, 5):
        for datum in data:
            boxes_truth = datum['truth'].boxes
            boxes_pred = datum['prediction'].boxes

            num_det += len(boxes_pred)
            # Check rank 0 first.
            num_hit += get_num_hit_rank(boxes_truth, boxes_pred, rank)

        print('>> To Rank', rank)
        print('>> Num rel = {r}, Num det = {d}, num hit = {h}.'.format(
            r=num_rel, d=num_det, h=num_hit))
        print('>> Precision = {p}, Recall = {r}'.format(
            p=num_hit / num_det, r=num_hit / num_rel))
        print('---------------------------------------------------------')
