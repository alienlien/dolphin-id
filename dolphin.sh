#!/bin/bash
flow --model ./config/tiny-yolo-dolphin.cfg \
    --config ./config/ \
    --load ./bin/tiny-yolo-voc.weights \
    --labels labels_dolphin.txt \
    --train \
    --annotation ./data/bounding-box/train/annotation \
    --dataset ./data/bounding-box/train/image
