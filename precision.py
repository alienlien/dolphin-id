#!/usr/env/python3
# This file calculate the prediction result.
# TODO: Unify all the names:
#       (Ground Truth, Prediction) v.s. (Relevant, Detection)

IOU_THRESHOLD = 0.5
MEAN_AVERAGE_PRECISION_GRIDS = [
    0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0
]


def is_overlap(box_1, box_2, iou_th):
    """It checks whether the boxes input are overlapped to each other
    or not. Note that the two boxes are called overlapped if their iou
    is higher than the threshold input.

    Args:
        box_1, box_2: The boxes input.
        iou_th: The threshold for the iou.
    """
    return box_1.iou(box_2) > iou_th


def get_num_hit(boxes_truth, boxes_pred, is_hit):
    """It returns the number of boxes 'hit' input.

    Args:
        boxes_1, boxes_2: The two sets of boxes input.
        is_hit: The func to check if the boxes are 'hit' to each other or not.
    """
    out = 0
    for tbox in boxes_truth:
        for pbox in boxes_pred:
            if is_hit(tbox, pbox):
                out += 1
    return out


def get_recall_precision(imgs_truth, imgs_pred, is_hit):
    """It returns the recall and precision for the images input.

    Args:
        imgs_truth: The images containing ground truth.
        imgs_pred: The images containing prediction boxes.
        is_hit: The func to check whether the boxes are hit or not.

    Returns:
        Recall, Precision.
    """
    # Numbers of relevant and detect boxes, respectively.
    num_rel = sum([len(img.boxes) for img in imgs_truth])
    num_det = sum([len(img.boxes) for img in imgs_pred])

    boxes_for_fname_truth = {img.fname: img.boxes for img in imgs_truth}
    boxes_for_fname_pred = {img.fname: img.boxes for img in imgs_pred}

    num_hit = 0
    for fname, boxes in boxes_for_fname_truth.items():
        if fname not in boxes_for_fname_pred:
            continue

        num_hit += get_num_hit(boxes, boxes_for_fname_pred[fname], is_hit)

    return num_hit / num_rel, num_hit / num_det


def is_equal(l1, l2):
    return l1 == l2


def is_label_match_rank(box_truth, box_pred, rank):
    if rank >= len(box_pred.pred_labels()):
        return False

    return box_truth.label() == box_pred.pred_labels()[rank]['label']


def get_hit_rank(box_pred,
                 boxes_truth,
                 topn,
                 iou_th=IOU_THRESHOLD,
                 is_match=is_equal):
    """It returns the rank that the labels predicted matches the ground truth.
    1) Go through all the boxes in img_truth, find the box
       with highest iou as the candidate.
    2) Check whether some label predicted matches the candidate's label.
    3) It returns the rank if some label matches the ground truth.

    Args:
        box_pred: The box containing the labels predicted.
        boxes_truth: All the possible ground truth boxes.
        topn: Top n labels to considered.
        iou_th: The threshould for iou.
        is_match: The func to define whether the boxes matches or not.

    Return:
        {
            'max_iou': The max iou with all the boxes in boxes_truth.
            'is_box_detected': Whether these is a box is detected or not.
            'rank': The rank of the label matched. -1: No match at any rank.
            'label': The label matched. Empty string: No match at any rank.
        }
        1) If all of the ground truth boxes has low iou with
           the prediction box, it returns (max_iou, False, -1, '').
        2) If some ground truth box has high iou with the one predicted,
           but there is no label matched, it returns (max_iou, True, -1, '').
        3) If some ground truth box has high iou with the one predicted,
           and some label predicted matches the one in ground truth,
           it returns (max_iou, True, rank, matched_label),
           ranks = 0, 1, ..., topn-1.
    """
    # Go through all the boxes of ground truth.
    # Find the one with max iou as the candidate.
    max_iou = 0.0
    for box in boxes_truth:
        iou = box_pred.iou(box)
        if iou > max_iou:
            candidate = box
            max_iou = iou

    # If there is no box overlapped, it returns the result directly.
    if max_iou == 0.0:
        return {
            'max_iou': 0.0,
            'is_box_detected': False,
            'rank': -1,
            'label': '',
        }

    # Check the rank the labels predicted match the ground truth.
    # Note that we check the labels whether the max_iou
    # is greater than the threshold or not since we want to analyze
    # the results for the localization error case (right label, low iou)
    pred_labels = [x['label'] for x in box_pred.pred_labels()]
    truth_label = candidate.label()
    for i in range(0, min(topn, len(pred_labels))):
        print('>> Label to check: Predict: {}, Truth: {}'.format(
            pred_labels[i], truth_label))
        if is_match(pred_labels[i], truth_label):
            return {
                'max_iou': max_iou,
                'is_box_detected': (max_iou > iou_th),
                'rank': i,
                'label': pred_labels[i],
            }

    # If all the labels predicted are not matched to the ground truth,
    # it returns rank '-1' to identify that there is no match.
    return {
        'max_iou': max_iou,
        'is_box_detected': (max_iou > iou_th),
        'rank': -1,
        'label': '',
    }


def get_num_hit_rank(boxes_truth, boxes_pred, rank):
    """It returns the number of hit of boxes on rank input.

    Args:
        boxes_truth: Ground truth boxes.
        boxes_pred: Boxes of prediction.
        rank: The rank to check. It begins from 0.

    Returns:
        It returns the number of boxes hits on the rank input.
    """

    def is_hit(box_truth, box_pred):
        return is_label_match_rank(box_truth, box_pred, rank)

    return get_num_hit(boxes_truth, boxes_pred, is_hit)


def get_average_precision(pairs, grids=MEAN_AVERAGE_PRECISION_GRIDS):
    """It returns the average precision for the list of
    precision-to-recall pairs.
    Ref: The PASCAL Visual Object Classes (VOC) Challenge.

    Args:
        Pairs: The list of precision-to-recall pairs
        {
            'precision': 0.35,
            'recall': 0.50,
        }, ...
    """
    return (1.0 / len(grids)) * sum(
        [get_itpl_precision(x, pairs) for x in grids])


def get_itpl_precision(recall, pairs):
    """It returns the precision interpolated for the pairs input.

    Args:
        recall: The recall input.
        pairs: The precision-recall pairs input.

    Return:
        The interpolated precision for the recall input.
    """
    larger_pairs = list(filter(lambda x: x['recall'] >= recall, pairs))

    if len(larger_pairs) == 0:
        return 0.0

    return max([x['precision'] for x in larger_pairs])
