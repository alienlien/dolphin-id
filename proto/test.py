#!/usr/bin/env python3
import time
from google.protobuf import json_format
import image_pb2 as pb

if __name__ == '__main__':
    location = pb.Location()
    location.latitude = 23.954178
    location.longitude = 121.620550

    rect_prop_1 = pb.RectangleProperty()
    rect_prop_1.upper_left_x = 50
    rect_prop_1.upper_left_y = 100
    rect_prop_1.width = 200
    rect_prop_1.height = 300

    pred_11 = pb.Prediction()
    pred_11.dolphin_id = 'ku_007'
    pred_11.prob = 0.65

    pred_12 = pb.Prediction()
    pred_12.dolphin_id = '20170101_01'
    pred_12.prob = 0.35

    pred_21 = pb.Prediction()
    pred_21.dolphin_id = 'ku_121'
    pred_21.prob = 0.70

    pred_22 = pb.Prediction()
    pred_22.dolphin_id = 'ku_087'
    pred_22.prob = 0.20

    pred_23 = pb.Prediction()
    pred_23.dolphin_id = '20140101_02'
    pred_23.prob = 0.10

    region_1 = pb.Region()
    region_1.shape = pb.Region.RECTANGLE
    region_1.rectangle_property.CopyFrom(rect_prop_1)
    region_1.dolphin_id = 'ku_007'
    region_1.group_id = 9
    region_1.predictions.extend([pred_11, pred_12])

    rect_prop_2 = pb.RectangleProperty()
    rect_prop_2.upper_left_x = 2046
    rect_prop_2.upper_left_y = 1739
    rect_prop_2.width = 1024
    rect_prop_2.height = 640

    region_2 = pb.Region()
    region_2.shape = pb.Region.RECTANGLE
    region_2.rectangle_property.CopyFrom(rect_prop_2)
    region_2.dolphin_id = '20100702_03'
    region_2.group_id = 13
    region_2.predictions.extend([pred_21, pred_22, pred_23])

    image = pb.Image()
    image.url = 'http://localhost:1337/parse/files/1/ac646d1b62192a605834f6ec8793d71a_pic.jpg'
    image.filename = 'HL20120708_01_gg_096_IMG_2934.JPG'
    image.sighting = 'HL20120708_01'
    image.location.CopyFrom(location)
    image.photographer = 'Alien Lien'
    image.species = 'Grampus griseus'
    image.shot_ts = int(time.time())
    image.regions.extend([region_1, region_2])

    fin_image = pb.FinImage()
    fin_image.url = 'http://localhost:1337/parse/files/1/ac646d1b62192a605834f6ec8793d71a_fin.jpg'
    fin_image.dolphin_id = 'ku_007'
    fin_image.photo_id = pb.FinImage.LEFT
    fin_image.parent = 'ac646d1b62192'
    fin_image.predictions.extend([pred_11, pred_12])

    print(image)
    print(json_format.MessageToJson(image))
    print(fin_image)
    print(json_format.MessageToJson(fin_image))
