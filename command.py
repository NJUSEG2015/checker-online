#!/usr/bin/env python3

import os

def unzip(file_name):
    if file_name.endswith(".zip"):
        os.system("unzip " + file_name)
        return file_name[ : -4]

def run_make(path):
    os.chdir(path)
    os.system("make")

checker = "/Users/chen/Workspace/public/huawei-checker/clang-llvm/build/bin/huawei-checker"
def run_checker(path):
    if not os.path.exists("output"):
        os.mkdir("output")
    os.system("find . -name \"*.ast\" > astList.txt")
    os.system(checker + " astList.txt config.json output")

