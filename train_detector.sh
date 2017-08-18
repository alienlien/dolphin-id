#!/bin/bash
# It is used to train the fin detector for the dolphins
flow --model ./config/tiny-yolo-dolphin.cfg \
    --config ./config/ \
    --load ./bin/tiny-yolo-voc.weights \
    --labels labels_dolphin.txt \
    --train \
    --annotation ./data/detector/train/annotation \
    --dataset ./data/detector/train/image
