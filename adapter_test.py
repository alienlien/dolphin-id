#!/usr/bin/env python3
import adapter as adp
from box import Box
import proto.image_pb2 as pb

test_upper_left_x = 50
test_upper_left_y = 60
test_upper_left = (test_upper_left_x, test_upper_left_y)
test_width = 100
test_height = 200
test_pred_1 = {
    'label': 'julie',
    'prob': 0.6,
}
test_pred_2 = {
    'label': 'angela',
    'prob': 0.2,
}
test_pred_3 = {
    'label': 'arbit',
    'prob': 0.15,
}
test_preds = [
    test_pred_1,
    test_pred_2,
    test_pred_3,
]
test_box = Box(
    upper_left=test_upper_left,
    width=test_width,
    height=test_height,
    pred_labels=test_preds, )


def test_to_pb_prediction():
    expected = pb.Prediction()
    expected.dolphin_id = 'julie'
    expected.prob = 0.6
    assert adp.to_pb_prediction(test_pred_1) == expected


def test_to_pb_rectangle_property():
    expected = pb.RectangleProperty()
    expected.upper_left_x = test_upper_left_x
    expected.upper_left_y = test_upper_left_y
    expected.width = test_width
    expected.height = test_height
    assert adp.to_pb_rectangle_property(test_box) == expected


def test_to_pb_region():
    expected = pb.Region()
    expected.shape = pb.Region.RECTANGLE
    prop = pb.RectangleProperty()
    prop.upper_left_x = test_upper_left_x
    prop.upper_left_y = test_upper_left_y
    prop.width = test_width
    prop.height = test_height
    expected.rectangle_property.CopyFrom(prop)
    pred_1 = pb.Prediction()
    pred_1.dolphin_id = 'julie'
    pred_1.prob = 0.6
    pred_2 = pb.Prediction()
    pred_2.dolphin_id = 'angela'
    pred_2.prob = 0.2
    pred_3 = pb.Prediction()
    pred_3.dolphin_id = 'arbit'
    pred_3.prob = 0.15
    expected.predictions.extend([pred_1, pred_2, pred_3])
    assert adp.to_pb_region(test_box) == expected
