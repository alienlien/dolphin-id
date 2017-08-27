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


def get_num_overlap(boxes_1, boxes_2, is_hit):
    """It returns the number of boxes overlapped for two sets of boxes
    input.

    Args:
        boxes_1, boxes_2: The two sets of boxes input.
        is_hit: The func to check if it is hit for boxes or not.
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
    """
    imgs_map_ans = {img.fname: img for img in imgs_ans}
    imgs_map_pred = {img.fname: img for img in imgs_pred}

    num_rel = sum([len(img.boxes) for img in imgs_ans])
    num_det = sum([len(img.boxes) for img in imgs_pred])

    num_hit = 0
    for fname, img in imgs_map_ans.items():
        if fname not in imgs_map_pred:
            continue

        num_hit += get_num_overlap(img.boxes, imgs_map_pred[fname].boxes,
                                   is_hit)
    return num_hit / num_rel, num_hit / num_det
