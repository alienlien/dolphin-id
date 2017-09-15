#!/bin/bash
# It is used to train the fin detector for the dolphins
# TODO: Add the selection for the latest model or the original one.
# Ref: https://github.com/thtrieu/darkflow#training-new-model
flow --model ./config/yolo-dolphin.cfg \
    --config ./config/ \
    --load ./bin/yolo-voc.weights \
    --labels labels_dolphin.txt \
    --train \
    --annotation ./data/detector/train/annotation \
    --dataset ./data/detector/train/image
