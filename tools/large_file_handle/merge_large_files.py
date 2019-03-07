#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import functools


kDirExtent = "_files"


def get_parent_path(path):
    return os.path.abspath(os.path.join(path, os.pardir))


def merge_large_files(root, files):
    suffix_length = len(kDirExtent)
    file_path = root[:-suffix_length]

    if os.path.exists(file_path):
        back_file_path = file_path + ".bak"
        if os.path.exists(back_file_path):
            os.remove(back_file_path)
        os.rename(file_path, back_file_path)
        print("backup exists file to " + back_file_path)

    files = sorted(files, key=functools.cmp_to_key(cmp_file_name))
    with open(file_path, "wb") as out_file:
        for f in files:
            input_file_path = os.path.join(root, f)
            if ".bin" not in input_file_path:
                continue
            with open(input_file_path, "rb") as in_file:
                content = in_file.read()
                out_file.write(content)
    print("merge file done: " + file_path)


def main():
    cur_path = os.path.dirname(os.path.abspath(__file__))
    parent_path = get_parent_path(cur_path)
    src_path = get_parent_path(parent_path)
    import_path = os.path.join(src_path, "import")

    walk_dirs = os.walk(import_path)
    for root, dirs, files in walk_dirs:
        if kDirExtent not in root:
            continue    # 忽略其他文件夹
        merge_large_files(root, files)


def cmp_file_name(left, right):
    left_names = left.split(".")
    if len(left_names) < 2:
        return 1
    right_names = right.split(".")
    if len(right_names) < 2:
        return 1

    left_name = left_names[0]
    if len(left_name) < 1:
        return 1

    right_name = right_names[0]
    if len(right_name) < 1:
        return 1

    left_index = int(left_name)
    right_index = int(right_name)

    return left_index - right_index


if __name__ == '__main__':
    main()
