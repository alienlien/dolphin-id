#!/usr/bin/env python3
from box import Box

test_label = 'test_111'
test_label2 = 'test_222'
test_upper_left = (13.0, 17.0)
test_lower_right = (42.0, 53.0)
test_center = (27.5, 35.0)
test_width = 29.0
test_height = 36.0
test_box = Box(
    label=test_label,
    center=test_center,
    width=test_width,
    height=test_height, )
test_box_no_overlap_x = Box(
    label=test_label2,
    center=(test_center[0], test_center[1] + test_height + 1),
    width=test_width,
    height=test_height, )
test_box_no_overlap_y = Box(
    label=test_label2,
    center=(test_center[0], test_center[1] + test_height + 1),
    width=test_width,
    height=test_height, )
test_box_overlap = Box(
    label=test_label2,
    upper_left=(29, 26),
    lower_right=(87, 66), )


def assert_box(b):
    assert b.upper_left() == test_upper_left
    assert b.lower_right() == test_lower_right
    assert b.center() == test_center
    assert b.width() == test_width
    assert b.height() == test_height


def test_box_init_1():
    b = Box(
        label=test_label,
        upper_left=test_upper_left,
        lower_right=test_lower_right)
    assert_box(b)


def test_box_init_2():
    b = Box(
        label=test_label,
        center=test_center,
        width=test_width,
        height=test_height)
    assert_box(b)


def test_box_init_3():
    b = Box(
        label=test_label,
        upper_left=test_upper_left,
        lower_right=test_lower_right)
    assert_box(b)


def test_box_init_pred_labels():
    label_low_prob = {
        'label': 'aaa',
        'prob': 0.3,
    }
    label_high_prob = {
        'label': 'bbb',
        'prob': 0.6,
    }
    labels = [
        label_low_prob,
        label_high_prob,
    ]
    b = Box(
        label=test_label,
        upper_left=test_upper_left,
        lower_right=test_lower_right,
        pred_labels=labels, )
    expected = [
        label_high_prob,
        label_low_prob,
    ]
    assert b.pred_labels() == expected


def test_is_valid():
    assert test_box.is_valid()

    b = Box()
    assert not b.is_valid()


def test_area():
    assert test_box.area() == test_width * test_height
    assert test_box_overlap.area() == (87 - 29) * (66 - 26)


def test_area_intersection():
    # Test no overlap case 1: Boxes do not overlap on x axis.
    assert test_box.area_intersection(test_box_no_overlap_x) == 0
    assert test_box_no_overlap_x.area_intersection(test_box) == 0

    # Test no overlap case 2: Boxes do not overlap on y axis.
    assert test_box.area_intersection(test_box_no_overlap_y) == 0
    assert test_box_no_overlap_y.area_intersection(test_box) == 0

    # Test the case that boxes indeed overlap each other.
    assert test_box.area_intersection(test_box_overlap) == 351
    assert test_box_overlap.area_intersection(test_box) == 351


def test_area_union():
    assert test_box.area_union(test_box_no_overlap_x) == 2 * test_box.area()
    assert test_box.area_union(
        test_box_overlap) == test_box.area() + test_box_overlap.area() - 351


def test_iou():
    assert test_box.iou(test_box_no_overlap_x) == 0
    assert test_box.iou(test_box_overlap) == 351 / (29 * 36 + 58 * 40 - 351)
