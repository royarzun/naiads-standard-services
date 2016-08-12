# coding=utf-8

import os
from array import array
from time import strftime


def convert_to_root_array(list_array):
    return array('d', list_array)


def create_filename(path, filename):
    timestamp_str = strftime("%Y%m%d%H%M%S")
    return path + filename + "_" + timestamp_str + ".root"


def get_limits(list_array):
    return [float(list_array[0]), float(list_array[-1])]


def set_output_folder(path):
    if os.path.isdir(path) and os.access(path, os.W_OK):
        return path if path.endswith("/") else path + "/"
    else:
        raise IOError("Output directory not writable.")
