# coding=utf-8

from array import array
from time import strftime


def convert_to_root_array(list_array):
    return array('d', list_array)


def create_filename(hname):
    timestamp_str = strftime("%Y%m%d%H%M%S")
    return hname + "_" + timestamp_str + ".root"


def get_limits(list_array):
    return [float(list_array[0]), float(list_array[-1])]
