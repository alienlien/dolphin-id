#!/usr/bin/env python3
from box import Box

test_label = 'test'
test_upper_left = (13.0, 17.0)
test_lower_right = (42.0, 53.0)
test_center = (27.5, 35.0)
test_width = 29.0
test_height = 36.0


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
