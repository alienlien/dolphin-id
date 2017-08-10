#!/usr/bin/env python3
# This files is used to parse the boxes into the form darkflow needs.
from box import Box


def gen_val(option, *args):
    """It returns the value based on the option and arguments input.
    """
    option = option.lower()

    if option == 'min':
        return min(*args)
    if option == 'max':
        return max(*args)
    return sum(args) / len(args)


def squarize(box, option='avg'):
    """It returns a square box based on the box and the option input.
    Specifically, the box returns would have the same center as the box input,
    and the side length is determined according to the option input:
    min: The minimum of the width and height of the box input.
    avg: The average of the width and height of the box input.
    max: The maximum of the width and height of the box input.

    Args:
        box: The box input.
        option: The option for the side lenght of the square output.
    """
    side = gen_val(option, box.width(), box.height())
    return Box(label=box.label(), center=box.center(), width=side, height=side)
