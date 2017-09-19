#!/usr/bin/env python3
# It benchmarks the performances for the system.
# TODO: Add docopt for options (folders, is_fin/is_match, ... etc.)
import os
import os.path
import sys
from box import ImageBoxes
from box import crop_image_for_box
from classifier import Classifier
from config import ConfigStore
from detector import FinDetector
from parser import xml_fname_from_jpg, from_xml
from precision import get_hit_rank, get_average_precision

IMG_FOLDER = os.path.abspath('./data/detector/validation/image/')
ANNO_FOLDER = os.path.abspath('./data/detector/validation/annotation/')
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


def is_match_ku_or_others(l1, l2):
    """It checks whether labels are matched to each other or not
    and the results depends on that they belong to group 'ku' or not.

    Args:
        l1, l2: The labels input.

    Returns:
        1) If both l1 and l2 belong to group 'ku', it checks whether
           they are of the same label or not.
        2) If both l1 and l2 do not belong to group 'ku', it returns True
           anyway since they belong to 'others'.
        3) If only one of the labels belongs to group 'ku', it returns False
           anyway since they belong to two different groups: 'ku' and 'others'.
    """
    if is_ku(l1) and is_ku(l2):
        return l1 == l2

    if (not is_ku(l1)) and (not is_ku(l2)):
        return True

    return False


def is_ku(label):
    """It checks whether the label belongs to group 'ku' or not.
    """
    return label.startswith('ku_')


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
#             result = get_hit_rank(
#                 box, datum['truth'].boxes, 5, is_match=is_match_ku_or_others)
            result = get_hit_rank(
                box, datum['truth'].boxes, 5)
            print('>> Result:', result)
            box_list.append(result)
        datum['results'] = box_list
        results[datum['prediction'].fname] = box_list
        print('---------------------------------------')

    for k, v in results.items():
        print('Key:', k)
        print('>> Values:')
        for x in v:
            print(x)
        print('-' * 40)

    mean_ap_data = {}

    # Collect information needed for recall and precision.
    num_truth_map = {}
    for idx, datum in enumerate(data):
        # Number of ground truth.
        for box in datum['truth'].boxes:
            label = box.label()
            if label not in num_truth_map:
                num_truth_map[label] = 0
            num_truth_map[box.label()] += 1
    mean_ap_data['num_truth'] = num_truth_map

    #     print('>> Num_truth_map:')
    #     for key, val in num_truth_map.items():
    #         print('Key: {}, Val: {'.format(key, val))
    #         print('-' * 40)
    #
    # Number of prediction.
    num_pred_map = {}
    for idx, datum in enumerate(data):
        for box in datum['prediction'].boxes:
            # TODO: Replace '5' to parameter/config top n.
            for rank in range(0, 5):
                key = (rank, box.pred_labels()[rank]['label'])
                if key not in num_pred_map:
                    num_pred_map[key] = 0
                num_pred_map[key] += 1
    mean_ap_data['num_pred'] = num_pred_map

    #     print('>> Num_pred_map:')
    #     for key, val in num_pred_map.items():
    #         print('Key: {}, Val: {}'.format(key, val))
    #         print('-' * 40)
    #
    # Number of hits.
    num_hit_map = {}
    for idx, datum in enumerate(data):
        for result in datum['results']:
            if result['rank'] >= 0:
                key = (result['rank'], result['label'])
                if key not in num_hit_map:
                    num_hit_map[key] = 0
                num_hit_map[key] += 1
    mean_ap_data['num_hit'] = num_hit_map

    #     print('>> Num_hit_map:')
    #     for key, val in num_hit_map.items():
    #         print('Key: {}, Val: {}'.format(key, val))
    #         print('-' * 40)
    #
    labels = sorted(mean_ap_data['num_truth'].keys())

    # TODO: Fix the problem that multiple boxes predicted points to
    # the same box and thus recall would be higher than 1.0.
    print('-' * 80)
    print('[ Precision-Recall by (Label, Rank)]')
    summary = {}
    for label in labels:
        num_truth = mean_ap_data['num_truth'][label]
        acc_num_hit = 0
        acc_num_pred = 0
        summary[label] = {
            'prec_recall': [],
            'map': 0.0,
        }
        for rank in range(0, 5):
            key = (rank, label)
            acc_num_hit += mean_ap_data['num_hit'].get(key, 0)
            acc_num_pred += mean_ap_data['num_pred'].get(key, 0)

            precision = acc_num_hit / acc_num_pred if acc_num_pred > 0 else 0.0
            recall = acc_num_hit / num_truth if num_truth > 0 else 0.0
            print('>> Label: {}, Rank: {}'.format(label, rank))
            print('>>   Acc Num Hit: {}, Acc Num Pred: {}, Num Truth: {}'.
                  format(acc_num_hit, acc_num_pred, num_truth))
            print('>>   Precision: {0:.3f}, Recall: {1:.3f}'.format(
                precision, recall))
            summary[label]['prec_recall'].append({
                'precision': precision,
                'recall': recall,
            })
        print('-' * 80)

    for label in labels:
        summary[label]['map'] = get_average_precision(summary[label]['prec_recall'])
        print('>> Label: {0}, ap: {1:.3f}, prec_recall: {2}'.format(label, summary[label]['map'], summary[label]['prec_recall']))

    mean_ap = 0.0
    total_truth = sum(mean_ap_data['num_truth'].values())
    for label in labels:
        mean_ap += summary[label]['map'] * mean_ap_data['num_truth'][label]
    mean_ap = mean_ap / total_truth
    print('--------------------------')
    print('>> MAP: ', mean_ap)

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

        num_hit += sum([
            1 for x in total_results
            if x['is_box_detected'] and (x['rank'] == rank)
        ])
        print('>> [Num] Truth: {}, pred: {}, hit: {}'.format(
            num_truth, num_pred, num_hit))
        print('>> Precision = {}, Recall = {}, Image Accuracy: {}'.format(
            num_hit / num_pred, num_hit / num_truth, num_hit / num_pred_box))
