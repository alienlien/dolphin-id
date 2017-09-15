#!/usr/bin/env python3
# It benchmarks the performances for the system.
import os
import os.path
import sys
from box import ImageBoxes
from box import crop_image_for_box
from classifier import Classifier
from config import ConfigStore
from detector import FinDetector
from parser import xml_fname_from_jpg, from_xml
from precision import get_hit_rank

IMG_FOLDER = os.path.abspath('./data/detector/test_id/validation/image/')
ANNO_FOLDER = os.path.abspath('./data/detector/test_id/validation/annotation/')
IOU_THRESHOLD = 0.5
DEFAULT_CFG_KEY = 'dolphin'


def is_fin(l1, l2):
    return True


def is_classifier_match_or_others(l1, l2):
    """It checks whether labels matches for the dolphins in ku groups
    that the classifier saw or not.

    Args:
        l1, l2: Labels 1 & 2.

    Returns:
        - If l1 and l2 are both known by the classifier, it returns
          whether they are the same or not.
        - If l1 and l2 are both not known by the classifier, it returns
          true since they all belong to the group 'Others'.
        - If they belongs to different groups, return false.
    """
    if is_classifier_seen(l1) and is_classifier_seen(l2):
        return l1 == l2

    # We return true no matter what the label is
    # if it is not belongs to ku group.
    if (not is_classifier_seen(l1)) and (not is_classifier_seen(l2)):
        return True

    # If the labels belongs to different groups, they are not matched.
    return False


def is_classifier_seen(l):
    return l in [
        'ku_000', 'ku_014', 'ku_015', 'ku_016', 'ku_017', 'ku_018', 'ku_020',
        'ku_022', 'ku_114', 'ku_178'
    ]


if __name__ == '__main__':
    config = ConfigStore().get(DEFAULT_CFG_KEY)
    classifier = Classifier(config)
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
        if idx % 10 == 0:
            print('>> Begining to predict {}th item...'.format(idx))

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

    print('-' * 40)

    results = {}
    for idx, datum in enumerate(data):
        box_list = []
        for box in datum['prediction'].boxes:
            print('>> Prediction Box:', box)
            print('>> Ground Truth  :', datum['truth'].boxes)
            #             result = get_hit_rank(
            #                 box, datum['truth'].boxes, 5, is_match=is_fin)
            result = get_hit_rank(
                box,
                datum['truth'].boxes,
                5,
                is_match=is_classifier_match_or_others)
            print('>> Result:', result)
            box_list.append(result)
        results[datum['prediction'].fname] = box_list
        print('---------------------------------------')

    for k, v in results.items():
        print('Key:', k)
        print('>> Values:', v)
        print('-' * 40)

    total_results = []
    for x in results.values():
        total_results += x

    num_truth = sum([len(x['truth'].boxes) for x in data])
    num_pred_box = sum([len(x['prediction'].boxes) for x in data])
    num_pred = 0
    num_hit = 0
    for rank in range(0, 5):
        num_pred += num_pred_box
        print('>> To rank: ', rank)

        num_hit += sum([1 for x in total_results if x[1] and (x[2] == rank)])
        print('>> [Num] Truth: {}, pred: {}, hit: {}'.format(
            num_truth, num_pred, num_hit))
        print('>> Precision = {}, Recall = {}, Image Accuracy: {}'.format(
            num_hit / num_pred, num_hit / num_truth, num_hit / num_pred_box))
