#!/bin/bash
# It is used to train the fin detector for the dolphins
# TODO: Add the selection for the latest model or the original one.
# Ref: https://github.com/thtrieu/darkflow#training-new-model
# NOTE: Remember to modify use option '--load -1' to continue or not.
flow --model ./config/yolo-dolphin.cfg \
    --config ./config/ \
    --load ./bin/yolo-voc.weights \
    --labels labels_dolphin.txt \
    --train \
    --annotation ./data/detector/train/annotation \
    --dataset ./data/detector/train/image
