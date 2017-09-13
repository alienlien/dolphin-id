#!/bin/bash
# Note that the classifier would fine tune the upper half of the model
# after lower half of the model finished training of the [nb_epoch] epochs.
# As a result, nb_epoch cannot be set too large.
python ./train_classifier.py \
    --train_dir=./data/classifier/train/ \
    --val_dir=./data/classifier/validation/ \
    --nb_epoch=50 \
    --batch_size=16 \
    --output_model_file=./model/dolphin_classifier.h5
