#!/usr/env/python3
# This file calculate the prediction result.

IOU_THRESHOLD = 0.5


def is_overlap(box_1, box_2, iou_th):
    """It checks whether the boxes input are overlapped to each other
    or not. Note that the two boxes are called overlapped if their iou
    is higher than the threshold input.

    Args:
        box_1, box_2: The boxes input.
        iou_th: The threshold for the iou.
    """
    return box_1.iou(box_2) > iou_th


def get_num_hit(boxes_1, boxes_2, is_hit):
    """It returns the number of boxes 'hit'.
    input.

    Args:
        boxes_1, boxes_2: The two sets of boxes input.
        is_hit: The func to check if the boxes are 'hit' to each other or not.
    """
    out = 0
    for b1 in boxes_1:
        for b2 in boxes_2:
            if is_hit(b1, b2):
                out += 1
    return out


def get_recall_precision(imgs_ans, imgs_pred, is_hit):
    """It returns the recall and precision for the images input.

    Args:
        imgs_ans: The images containing answers.
        imgs_pred: The images containing prediction boxes.
        is_hit: The func to check whether the boxes are hit or not.

    Returns:
        Recall, Precision.
    """
    # Numbers of relevant and detect boxes, respectively.
    num_rel = sum([len(img.boxes) for img in imgs_ans])
    num_det = sum([len(img.boxes) for img in imgs_pred])

    boxes_for_fname_ans = {img.fname: img.boxes for img in imgs_ans}
    boxes_for_fname_pred = {img.fname: img.boxes for img in imgs_pred}

    num_hit = 0
    for fname, boxes in boxes_for_fname_ans.items():
        if fname not in boxes_for_fname_pred:
            continue

        num_hit += get_num_hit(boxes, boxes_for_fname_pred[fname], is_hit)

    return num_hit / num_rel, num_hit / num_det
