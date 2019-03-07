#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys


kMaxFileSize = 45 * 1000 * 1000
kDirExtent = "_files"


def get_parent_path(path):
    return os.path.abspath(os.path.join(path, os.pardir))


def is_large_file(file_path):
    file_size = os.path.getsize(file_path)
    if file_size > kMaxFileSize:
        return True
    return False


def split_large_file(file_path):
    # input_file_name = os.path.basename(file_path)
    sub_file_dir_path = file_path + kDirExtent
    is_dir_exists = os.path.isdir(sub_file_dir_path)
    if not is_dir_exists:
        os.mkdir(sub_file_dir_path)

    with open(file_path, "rb") as file_handle:
        should_continue = True
        index = 0
        while should_continue:
            bytes_content = file_handle.read(kMaxFileSize)
            if len(bytes_content) < kMaxFileSize:
                should_continue = False
            output_file_name = "%d.bin" % index
            child_file_path = os.path.join(sub_file_dir_path, output_file_name)
            with open(child_file_path, "wb") as out_file:
                out_file.write(bytes_content)
            index = index + 1
            print("write to %s done" % child_file_path)


def handle_files(root, files):
    for f in files:
        file_path = os.path.join(root, f)
        if not is_large_file(file_path):
            continue
        print("processing " + file_path)
        split_large_file(file_path)


def main():
    cur_path = os.path.dirname(os.path.abspath(__file__))
    parent_path = get_parent_path(cur_path)
    src_path = get_parent_path(parent_path)
    import_path = os.path.join(src_path, "import")

    walk_dirs = os.walk(import_path)
    for root, dirs, files in walk_dirs:
        if kDirExtent in root:
            continue    # 忽略子文件夹
        handle_files(root, files)


if __name__ == '__main__':
    main()
