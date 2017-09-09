#!/usr/bin/env python3
# from copy import deepcopy
from box import Box
import precision as p

test_iou_threshold = 0.3
test_upper_left_x = 50
test_upper_left_y = 60
test_upper_left = (test_upper_left_x, test_upper_left_y)
test_width = 100
test_height = 200
test_box_pred = Box(
    upper_left=test_upper_left,
    width=test_width,
    height=test_height,
    pred_labels=[{
        'label': 'julie',
        'prob': 0.6,
    }, {
        'label': 'angela',
        'prob': 0.2,
    }, {
        'label': 'arbit',
        'prob': 0.15,
    }, {
        'label': 'taco',
        'prob': 0.05,
    }])
test_box_low_iou = Box(
    label='julie',
    upper_left=test_upper_left,
    width=test_width * 5,
    height=test_height * 10, )
test_box_high_iou = Box(
    label='angela',
    upper_left=test_upper_left,
    width=test_width / 4,
    height=test_height / 2, )
test_box_no_overlap = Box(
    label='arbit',
    upper_left=(test_upper_left_x + test_width, test_upper_left_y),
    width=test_width,
    height=test_height, )
test_boxes_truth = [test_box_low_iou, test_box_high_iou, test_box_no_overlap]


def test_get_hit_rank_not_detected():
    """It test the case that the iou of all the boxes are
    lower than the threshold.
    """
    actual = p.get_hit_rank(
        test_box_pred, test_boxes_truth, topn=10, iou_th=0.9)
    # The candidate is the test_box_high_iou with iou 1 / (4 * 2)
    expected = (1 / (4 * 2), False, -1)
    assert actual == expected


def test_get_hit_rank_match_topn():
    """It tests the cases that it overlaps some box
    but the results depends on the choice of topn.
    """
    # Test the case that it overlaps some box but
    # the matched label is of the rank not covered by topn.
    actual = p.get_hit_rank(
        test_box_pred, test_boxes_truth, topn=1, iou_th=0.1)
    expected = (1 / (4 * 2), True, -1)
    assert actual == expected

    # Test the case that it overlaps some box and
    # it returns the rank of label predicted.
    actual = p.get_hit_rank(
        test_box_pred, test_boxes_truth, topn=3, iou_th=0.1)
    expected = (1 / (4 * 2), True, 1)
    assert actual == expected

    # Test the case that it overlaps some box and
    # the topn input is too large.
    actual = p.get_hit_rank(
        test_box_pred, test_boxes_truth, topn=100, iou_th=0.1)
    expected = (1 / (4 * 2), True, 1)
    assert actual == expected


def test_get_hit_rank_wrong_label():
    """It tests the case that it overlaps to some box
    but no label matches.
    """
    boxes_truth = [
        Box(
            label='no_one_matches',
            upper_left=test_upper_left,
            width=test_width,
            height=test_height)
    ]
    actual = p.get_hit_rank(test_box_pred, boxes_truth, topn=4, iou_th=0.9)
    expected = (1.0, True, -1)
    assert actual == expected
