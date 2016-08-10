# coding=utf-8

import json
from time import strftime

from ROOT import TH2F

from clara.base.ClaraUtils import ClaraUtils
from clara.engine.EngineDataType import EngineDataType, Mimetype
from clara.engine.Engine import Engine


class Histogram2dWriterService(Engine):

    def get_author(self):
        return "Ricardo Oyarzun <oyarzun@jlab.org>"

    def get_description(self):
        return "2D Histogram writer service, writes a ROOT file with histogram"

    def get_states(self):
        pass

    def get_output_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.STRING())

    def execute(self, engine_data):

        if engine_data.mimetype == Mimetype.STRING:
            json_object = json.loads(engine_data.get_data())

            x_limits = self._get_limits(json_object["xAxis"]["centers"])
            y_limits = self._get_limits(json_object["yAxis"]["centers"])

            histogram_name = json_object["annotation"]["Title"]
            histogram = TH2F("histogram",
                             histogram_name,
                             100, x_limits[0], x_limits[1],
                             100, y_limits[0], y_limits[1])

            for i, i_count in zip(json_object["xAxis"]["centers"],
                                  json_object["counts"]):
                for j, val in zip(json_object["yAxis"]["centers"],
                                  i_count):
                    histogram.Fill(i, j, val)

            histogram.SaveAs(self._create_filename(histogram_name))
            return histogram

        return engine_data

    def execute_group(self, inputs):
        pass

    def reset(self):
        pass

    def destroy(self):
        pass

    def get_version(self):
        return "v1.0"

    def get_input_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.STRING())

    def configure(self, engine_data):
        pass

    def _create_filename(self, name_label):
        timestamp_str = strftime("%Y%m%d%H%M%S")
        return name_label + "_" + timestamp_str + ".root"

    def _get_limits(self, list_array):
        return [float(list_array[0]), float(list_array[-1])]
