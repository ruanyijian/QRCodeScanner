#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xml.etree.cElementTree as etree
import datetime

TARGET_SRC_ROOT = "../src"
TARGET_PROJECT_NAMES = ["organic"]
TARGET_PLIST_FILES = ["Info.plist"]
DEBUG_ENABLE = False

def get_value_node_by_key(dict_node, key):
    key_node = None
    value_node = None
    for key_value_node in dict_node:
        text = key_value_node.text
        if text == key:
            key_node = key_value_node
            continue
        if key_node is not None:
            value_node = key_value_node
            break

    return value_node
    

def get_version_string(root):
    dict_node = root.find("dict")
    if not dict_node:
        return ""

    version_string_node = get_value_node_by_key(dict_node, "CFBundleVersion")
    if version_string_node is None:
        return ""

    return version_string_node.text


def get_version_code(root):
    dict_node = root.find("dict")
    if not dict_node:
        return ""

    version_value_node = get_value_node_by_key(dict_node, "CFBundleShortVersionString")
    if version_value_node is None:
        return ""

    return version_value_node.text


def replace_version_code(file_path, old_version_code, new_version_code):
    file_content = None
    with open(file_path, "rb") as f:
        file_content = f.read()

    if not isinstance(file_content, str):
        print("file_content is not instance of str, actually: %s" % type(file_content))
        return False

    if DEBUG_ENABLE:
        print("old_version_code: " + old_version_code)
        print("new_version_code: " + new_version_code)

    file_content = file_content.replace(old_version_code, new_version_code)
    with open(file_path, "wb") as f:
        f.write(file_content)

    return True


# 根据旧的版本号生成新的版本号
# 项目要求格式是 YYMMDD + Build，如 16010102
# 表示 2016 年 1 月 1 日 第二次构建的版本
def generate_new_version_string(old_version_string):
    if not isinstance(old_version_string, str):
        print("old_version_string is not instance of str, actually: %s" % type(old_version_string))
        return None

    if len(old_version_string) != 8:
        print("old_version_string length is expect like YYMMDDbb, actually: %s" % type(old_version_string))
        return None

    date_code = old_version_string[0:6]
    build_code = old_version_string[6:]
    int_build_code = int(build_code)

    today = datetime.date.today()
    new_date_code = today.strftime("%Y%m%d")
    new_date_code = new_date_code[2:]
    if new_date_code == date_code:
        int_build_code += 1
    else:
        int_build_code = 1

    new_build_code = str(int_build_code).zfill(2)
    new_version_code = new_date_code + new_build_code

    return new_version_code


# 根据旧的版本号生成修复包的版本号
# 修复包 (a.b.c, c > 0) 要求不能更新日期域，只能更新Build域
def generate_fix_version_string(old_version_string):
    if not isinstance(old_version_string, str):
        return None

    if len(old_version_string) != 8:
        return None

    date_code = old_version_string[0:6]
    build_code = old_version_string[6:]
    int_build_code = int(build_code)
    int_build_code += 1

    new_build_code = str(int_build_code).zfill(2)
    new_version_code = date_code + new_build_code

    return new_version_code


def generate_version_string(version_code, version_string):
    result_version_string = version_string
    version_codes = version_code.split('.')
    if len(version_codes) != 3:
        print("invalid version_codes, should be x.y.z, actually: %s" % version_codes)
        return result_version_string

    fix_code_string = version_codes[2]
    fix_code_int = int(fix_code_string)
    if fix_code_int == 0:
        result_version_string = generate_new_version_string(version_string)
    else:
        result_version_string = generate_fix_version_string(version_string)

    return result_version_string


def update_version(plist_file_path):
    if not isinstance(plist_file_path, str):
        return False

    xml_tree = etree.ElementTree(file=plist_file_path)
    if not xml_tree:
        return False

    root = xml_tree.getroot()
    version_code = get_version_code(root)
    version_string = get_version_string(root)
    if not isinstance(version_code, str):
        return False

    new_version_string = generate_version_string(version_code, version_string)
    result = replace_version_code(plist_file_path, version_string, new_version_string)

    return result


def file_log(message):
    current_dir = os.path.realpath(os.path.dirname(__file__))
    path = os.path.join(current_dir, "log.txt")
    with open(path, "a+") as f:
        f.write(message)
        f.write("\r\n")


# def commit_files(plist_files):
#     commit_command = """svn ci -m "* auto update version script" """
#     for plist_file in plist_files:
#         commit_command += '"' + plist_file + '" '
#     os.system(commit_command)
#     file_log("exec command " + commit_command)


def main():
    current_dir = os.path.realpath(os.path.dirname(__file__))
    plist_files = []
    for project_name in TARGET_PROJECT_NAMES:
        path = os.path.join(TARGET_SRC_ROOT, project_name)
        path = os.path.join(current_dir, path)
        for plist_file in TARGET_PLIST_FILES:
            plist_path = os.path.join(path, plist_file)
            plist_path = os.path.abspath(plist_path)
            update_version(plist_path)
            plist_files.append(plist_path)
    # commit_files(plist_files)


if __name__ == '__main__':
    main()
