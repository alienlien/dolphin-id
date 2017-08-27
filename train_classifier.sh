#!/bin/bash
python ./train_classifier.py \
    --train_dir=./data/train/ \
    --val_dir=./data/validation/ \
    --nb_epoch=500 \
    --batch_size=16 \
    --output_model_file=./model/dolphin_classifier.h5
