#!/usr/env/python3
# This file calculate the prediction result.
# TODO: Unify all the names:
#       (Ground Truth, Prediction) v.s. (Relevant, Detection)


def is_overlap(box_1, box_2, iou_th):
    """It checks whether the boxes input are overlapped to each other
    or not. Note that the two boxes are called overlapped if their iou
    is higher than the threshold input.

    Args:
        box_1, box_2: The boxes input.
        iou_th: The threshold for the iou.
    """
    print('>> IOU:', box_1.iou(box_2))
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


def is_label_match_rank(box_truth, box_pred, rank):
    if rank >= len(box_pred.pred_labels()):
        return False

    return box_truth.label() == box_pred.pred_labels()[rank]['label']


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
