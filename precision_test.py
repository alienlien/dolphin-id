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
# Note that we put two items with the same recall but different precision.
test_precision_recall_pairs = [{
    'precision': 0.8,
    'recall': 0.25,
}, {
    'precision': 0.6,
    'recall': 0.4,
}, {
    'precision': 0.1,
    'recall': 0.7,
}, {
    'precision': 0.4,
    'recall': 0.95,
}, {
    'precision': 0.2,
    'recall': 0.95,
}, {
    'precision': 0.3,
    'recall': 1.0,
}]


def test_get_hit_rank_not_detected():
    """It test the case that the iou of all the boxes are
    lower than the threshold.
    """
    actual = p.get_hit_rank(
        test_box_pred, test_boxes_truth, topn=10, iou_th=0.9)
    # The candidate is the test_box_high_iou with iou 1 / (4 * 2)
    expected = {
        'max_iou': 1 / (4 * 2),
        'is_box_detected': False,
        'rank': -1,
        'label': '',
    }
    assert actual == expected


def test_get_hit_rank_match_topn():
    """It tests the cases that it overlaps some box
    but the results depends on the choice of topn.
    """
    # Test the case that it overlaps some box but
    # the matched label is of the rank not covered by topn.
    actual = p.get_hit_rank(
        test_box_pred, test_boxes_truth, topn=1, iou_th=0.1)
    expected = {
        'max_iou': 1 / (4 * 2),
        'is_box_detected': True,
        'rank': -1,
        'label': '',
    }
    assert actual == expected

    # Test the case that it overlaps some box and
    # it returns the rank of label predicted.
    actual = p.get_hit_rank(
        test_box_pred, test_boxes_truth, topn=3, iou_th=0.1)
    expected = {
        'max_iou': 1 / (4 * 2),
        'is_box_detected': True,
        'rank': 1,
        'label': 'angela',
    }
    assert actual == expected

    # Test the case that it overlaps some box and
    # the topn input is too large.
    actual = p.get_hit_rank(
        test_box_pred, test_boxes_truth, topn=100, iou_th=0.1)
    expected = {
        'max_iou': 1 / (4 * 2),
        'is_box_detected': True,
        'rank': 1,
        'label': 'angela',
    }
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
    expected = {
        'max_iou': 1.0,
        'is_box_detected': True,
        'rank': -1,
        'label': '',
    }
    assert actual == expected


def test_get_itpl_precision():
    # Test the case if the recall input is too large.
    assert p.get_itpl_precision(1.1, test_precision_recall_pairs) == 0.0

    # Test the case that there is at least one item with larger recall
    # than the one input.
    assert p.get_itpl_precision(0.5, test_precision_recall_pairs) == 0.4


def test_get_average_precision():
    pairs = test_precision_recall_pairs
    grids = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    assert abs(p.get_average_precision(pairs, grids) - 0.55) < 1e-6
