#!/usr/bin/env python3
# It benchmarks the performances for the system.
# TODO: Add docopt for options (folders, is_fin/is_match, ... etc.)
import os
import os.path
import sys
from docopt import docopt
from PIL import Image
from box import ImageBoxes
from box import crop_image_for_box
from classifier import Classifier
from config import ConfigStore
from detector import FinDetector
from draw import BoxDrawer
from parser import xml_fname_from_jpg, from_xml
from precision import get_hit_rank, get_average_precision, is_equal

IOU_THRESHOLD = 0.5
DEFAULT_CFG_KEY = 'dolphin'
COLOR_CORRECT = 'green'
COLOR_LOCALIZATION = 'yellow'
COLOR_OTHER = 'orange'
COLOR_BACKGROUND = 'red'
COLOR_GROUND_TRUTH = 'white'


def is_fin(l1, l2):
    return True


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


def is_match_type(tp):
    """It returns the is_match function for the type input.

    Args:
        tp: Type of the is_match function.
    """
    if tp == 'fin':
        return is_fin
    if tp == 'ku':
        return is_match_ku_or_others
    return is_equal


def is_error_localization(result):
    """It checks whether the result is a localization error or not.
    Note that the types of the error comes from the yolo paper.
    Ref: https://pjreddie.com/media/files/papers/yolo.pdf
    """
    return result['max_iou'] >= 0.1 and result['rank'] >= 0 and not result['is_box_detected']


def is_error_other(result):
    """It checks whether the result is an other erro or not.
    """
    return result['max_iou'] >= 0.1 and result['rank'] == -1


def is_error_background(result):
    """It checks whether the result is an background error or not.
    """
    return result['max_iou'] < 0.1


usage = """
Usage:
    benchmark.py [options]

Options:
    --imgdir=DIR    The directory contains images [default: ./data/detector/train/image/]
    --annodir=DIR   The directory contains annotations [default: ./data/detector/train/annotation/]
    --outdir=DIR    The directory containing output images.
    --match=TYPE    The type for match function other than equal (fin, ku) [default: equal]
"""
if __name__ == '__main__':
    args = docopt(usage, help=True)
    img_folder = os.path.abspath(args['--imgdir'])
    anno_folder = os.path.abspath(args['--annodir'])
    out_folder = os.path.abspath(args.get('--outdir', ''))

    config = ConfigStore().get(DEFAULT_CFG_KEY)
    classifier = Classifier(config)
    detector = FinDetector()
    drawer = BoxDrawer()

    img_files = [x for x in os.listdir(img_folder)]
    anno_files = {x: True for x in os.listdir(anno_folder)}

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
                'image': os.path.join(img_folder, img_file),
                'annotation': os.path.join(anno_folder, anno_file),
                'out': os.path.join(out_folder, img_file),
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

    is_match = is_match_type(args['--match'])
    results = {}
    for idx, datum in enumerate(data):
        box_list = []
        for box in datum['prediction'].boxes:
            print('>> Prediction Box:', box)
            print('>> Ground Truth  :', datum['truth'].boxes)
            result = get_hit_rank(
                box, datum['truth'].boxes, 5, is_match=is_match)
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

    # Number of hits.
    num_hit_map = {}
    for idx, datum in enumerate(data):
        for result in datum['results']:
            if result['is_box_detected'] and result['rank'] >= 0:
                key = (result['rank'], result['label'])
                if key not in num_hit_map:
                    num_hit_map[key] = 0
                num_hit_map[key] += 1
    mean_ap_data['num_hit'] = num_hit_map

    # Collect the mis-labeled data for analysis.
    # - Localization: Low IOU but correct label.
    # - Other: Low IOU but wrong label.
    # - Background: Too low IOU.
    # TODO: Isolate it into a function?
    error_data = {
        'localization': 0,
        'other': 0,
        'background': 0,
    }
    for idx, datum in enumerate(data):
        for result in datum['results']:
            if is_error_localization(result):
                error_data['localization'] += 1

            if is_error_other(result):
                error_data['other'] += 1

            if is_error_background(result):
                error_data['background'] += 1

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
            summary[label]['prec_recall'].append({
                'precision': precision,
                'recall': recall,
            })

    for label in labels:
        summary[label]['map'] = get_average_precision(
            summary[label]['prec_recall'])
        print('>> Label: {0}, ap: {1:.3f}, prec_recall: {2}'.format(
            label, summary[label]['map'], summary[label]['prec_recall']))

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
        print(
            '>> Precision = {0:.3f}, Recall = {1:.3f}, Image Accuracy: {2:.3f}'.
            format(num_hit / num_pred, num_hit / num_truth, num_hit /
                   num_pred_box))
    print('>> Error Data:', error_data)

    if out_folder:
        for cntr, datum in enumerate(data):
            if cntr % 10 == 0:
                print('>> Drawing {0:>4d}th image...'.format(cntr))

            img_in = datum['files']['image']
            img_out = datum['files']['out']
            img = Image.open(img_in).copy()

            # Draw the prediction boxes, where the colors depending on
            # the prediction results.
            for idx, box in enumerate(datum['prediction'].boxes):
                result = datum['results'][idx]

                color = COLOR_CORRECT
                if is_error_localization(result):
                    color = COLOR_LOCALIZATION
                if is_error_other(result):
                    color = COLOR_OTHER
                if is_error_background(result):
                    color = COLOR_BACKGROUND

                if result['rank'] >= 0:
                    label = result['label']
                else:
                    label = box.pred_labels()[0]['label']

                box.set_label(label)
                img = drawer.draw(img, [box], color=color)

            # Draw the ground truth boxes.
            img = drawer.draw(
                img, datum['truth'].boxes, color=COLOR_GROUND_TRUTH)

            img.save(img_out)
