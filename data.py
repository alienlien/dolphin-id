#!/usr/bin/env python3
# It is used to arrange data.
import os
import os.path
import re
import shutil

DATA_FOLDER = './data/src/'
DATA_FOLDER_MERGE = './data/merge/'


def get_dolphin_id(s):
    pattern = r'Ku\ N(\d\d\d)|Ku(\d\d\d)'
    result = re.search(pattern, s)
    if not result:
        return ''

    if result.group(1):
        return result.group(1)
    return result.group(2)


if __name__ == '__main__':
    out = {}
    for root, dirs, files in os.walk(DATA_FOLDER):
        did = get_dolphin_id(root)
        if did:
            if did not in out:
                out[did] = []
            file_paths = [
                os.path.join(root, f) for f in files
                if f.lower().endswith('jpg')
            ]
            out[did] += file_paths

    if not os.path.exists(DATA_FOLDER_MERGE):
        os.mkdir(DATA_FOLDER_MERGE)

    for did, files in out.items():
        folder = os.path.join(DATA_FOLDER_MERGE, did)
        os.mkdir(folder)
        for name in files:
            des = os.path.join(folder, os.path.basename(name))
            shutil.copyfile(name, des)
