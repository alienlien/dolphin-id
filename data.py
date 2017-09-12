#!/usr/bin/env python3
# It is used to arrange data for classifier.
import os
import os.path
import re
import shutil

DATA_FOLDER = './data/classifier/src/'
DATA_FOLDER_MERGE = './data/classifier/merge/'


def get_dolphin_id(s):
    pattern = r'ku\ n(\d\d\d)|ku(\d\d\d)'
    result = re.search(pattern, s.lower())
    if not result:
        id_for_set = os.path.basename(s)
        data_set = os.path.basename(os.path.dirname(s))
        return '{set}_{id}'.format(set=data_set, id=id_for_set)

    if result.group(1):
        return kuroshio_id_for(result.group(1))
    return kuroshio_id_for(result.group(2))


def kuroshio_id_for(did):
    return 'ku_{id}'.format(id=did)


if __name__ == '__main__':
    # Make the dictionary that maps the dolphin id to
    # its corresponding pictures.
    out = {}
    for root, dirs, files in os.walk(DATA_FOLDER):
        if len(dirs) > 0 or 'poor' in root:
            continue

        did = get_dolphin_id(root)
        if did not in out:
            out[did] = []
        file_paths = [
            os.path.join(root, f) for f in files if f.lower().endswith('jpg')
        ]
        out[did] += file_paths

    if not os.path.exists(DATA_FOLDER_MERGE):
        os.mkdir(DATA_FOLDER_MERGE)

    # Copy the files to the corresponding folders.
    for did, files in out.items():
        folder = os.path.join(DATA_FOLDER_MERGE, did)
        os.mkdir(folder)
        for name in files:
            des = os.path.join(folder, os.path.basename(name))
            shutil.copyfile(name, des)
