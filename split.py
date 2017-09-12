#!/usr/bin/env python3
# This file splits the dataset into training and validation sets.
import os
import os.path
import shutil
import random

DATA_FOLDER = './data/classifier/merge'
TRAIN_FOLDER = './data/classifier/train'
VALIDATION_FOLDER = './data/classifier/validation'
MIN_VAL_NUM = 1
VAL_RATIO = 0.2
IS_SHUFFLE = True


def split_files(files, val_ratio, is_shuffle):
    """It splits the files into validation and training sets.

    Args:
        files: The list containing all the files.
        val_ratio: The ratio of validation sets.
        is_shuffle: Shuffle the order of the file list or not.

    Return:
        The map containing file lists for training and validation,
        respectively.
    """
    total_num = len(files)

    if is_shuffle:
        files = random.sample(files, total_num)

    val_num = max(int(float(total_num) * val_ratio), MIN_VAL_NUM)
    return {
        'train': files[val_num:],
        'validation': files[:val_num],
    }


def copy_files_to_folder(files, dst_dir):
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    for item in files:
        shutil.copy(item, dst_dir)


if __name__ == '__main__':
    for folder in [TRAIN_FOLDER, VALIDATION_FOLDER]:
        if not os.path.exists(folder):
            os.mkdir(folder)

    for root, dirs, files in os.walk(DATA_FOLDER):
        if len(dirs) > 0:
            continue

        base_name = os.path.basename(root)
        train_dir = os.path.join(TRAIN_FOLDER, base_name)
        val_dir = os.path.join(VALIDATION_FOLDER, base_name)
        files = [os.path.join(root, f) for f in files]
        result = split_files(files, VAL_RATIO, IS_SHUFFLE)

        copy_files_to_folder(result['train'], train_dir)
        copy_files_to_folder(result['validation'], val_dir)
