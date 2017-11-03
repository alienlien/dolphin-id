#!/usr/bin/env python3
# This file is the adapter for the protobuf objects.
import proto.image_pb2 as pb


def to_pb_prediction(pred):
    """It returns the Prediction defined in protobuf for pred_label input.
    """
    out = pb.Prediction()
    out.dolphin_id = pred['label']
    out.prob = pred['prob']
    return out


def to_pb_rectangle_property(box):
    """It returns the rectangle property in protobuf from box.
    """
    prop = pb.RectangleProperty()
    (prop.upper_left_x, prop.upper_left_y) = box.upper_left()
    prop.width = box.width()
    prop.height = box.height()
    return prop


def to_pb_region(box):
    """It returns the protobuf for the box input.
    """
    region = pb.Region()
    region.shape = pb.Region.RECTANGLE
    region.rectangle_property.CopyFrom(to_pb_rectangle_property(box))
    preds = [to_pb_prediction(x) for x in box.pred_labels()]
    region.predictions.extend(preds)
    return region
