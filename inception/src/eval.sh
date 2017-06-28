#!/bin/bash
# Build the model. Note that we need to make sure the TensorFlow is ready to
# use before this as this command will not build TensorFlow.
bazel build //inception:flowers_eval

# Directory where we saved the fine-tuned checkpoint and events files.
TRAIN_DIR=../model

# Directory where the flowers data resides.
FLOWERS_DATA_DIR=../flower_photos/

# Directory where to save the evaluation events files.
EVAL_DIR=/tmp/flowers_eval/

# Evaluate the fine-tuned model on a hold-out of the flower data set.
bazel-bin/inception/flowers_eval \
  --eval_dir="${EVAL_DIR}" \
  --data_dir="${FLOWERS_DATA_DIR}" \
  --subset=validation \
  --num_examples=500 \
  --checkpoint_dir="${TRAIN_DIR}" \
  --input_queue_memory_factor=1 \
  --run_once
