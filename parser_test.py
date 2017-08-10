#!/usr/bin/env python3
from parser import squarize, gen_val
from box import Box

test_label = 'test_label'
test_center = (128.0, 27.0)
test_width = 81.0
test_height = 24.0


def test_gen_val():
    assert gen_val('MIN', 19.0, 11.0, 33.0) == 11.0
    assert gen_val('Max', 19.0, 11.0, 33.0) == 33.0
    assert gen_val('average', 19.0, 11.0, 33.0) == 21.0


def test_squarize():
    box = Box(
        label=test_label,
        center=test_center,
        width=test_width,
        height=test_height, )

    actual = squarize(box, option='avg')
    expected = Box(
        label=test_label,
        center=test_center,
        width=52.5,
        height=52.5, )
    assert actual == expected
