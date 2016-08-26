# coding=utf-8

from ROOT import TH1F, TH2F

from naiads.utils.Utils import create_filename, get_limits,\
    convert_to_root_array


def create_1d_histogram(json_object, output_dir):
    limits = get_limits(json_object["xAxis"]["centers"])
    histogram_name = json_object["annotation"]["Title"]

    histogram = TH1F("histogram", histogram_name, 100, limits[0], limits[1])
    histogram.SetContent(convert_to_root_array(json_object["counts"]))
    histogram.SetError(convert_to_root_array(json_object["errors"]))
    histogram.SaveAs(create_filename(output_dir, histogram_name))


def create_2d_histogram(json_object, output_dir):
    x_limits = get_limits(json_object["xAxis"]["centers"])
    y_limits = get_limits(json_object["yAxis"]["centers"])

    histogram_name = json_object["annotation"]["Title"]
    histogram = TH2F("histogram", histogram_name,
                     100, x_limits[0], x_limits[1],
                     100, y_limits[0], y_limits[1])

    for i, i_count in zip(json_object["xAxis"]["centers"],
                          json_object["counts"]):
        for j, val in zip(json_object["yAxis"]["centers"],
                          i_count):
            histogram.Fill(i, j, val)
    histogram.SaveAs(create_filename(output_dir, histogram_name))
