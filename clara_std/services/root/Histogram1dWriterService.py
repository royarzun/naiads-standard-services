# coding=utf-8

import json
from array import *

from clara.base.ClaraUtils import ClaraUtils
from clara.engine.EngineDataType import EngineDataType, Mimetype
from clara.engine.Engine import Engine

from ROOT import TH1F


class Histogram1dWriterService(Engine):

    def get_author(self):
        return "Ricardo Oyarzun <oyarzun@jlab.org>"

    def get_description(self):
        return "Histogram writer services, writes a ROOT file with" \
               " event histogram"

    def get_states(self):
        return None

    def get_output_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.STRING())

    def execute(self, engine_data):

        if engine_data.mimetype == Mimetype.STRING:
            json_object = json.loads(engine_data.get_data())
            lower_limit = float(json_object["xAxis"]["centers"][0])
            upper_limit = float(json_object["xAxis"]["centers"][99])
            histo = TH1F("example", "example", 100, lower_limit, upper_limit)
            histo.SetContent(self._convertToRootArray(json_object["counts"]))
            histo.SetError(self._convertToRootArray(json_object["errors"]))

            histo.SaveAs("histos.root")
            return histo
        return None

    def execute_group(self, inputs):
        return None

    def reset(self):
        return None

    def destroy(self):
        """ Histogram should be created and histo object deleted """
        return None

    def get_version(self):
        return "v1.0"

    def get_input_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.STRING())

    def configure(self, engine_data):
        return None

    def _convertToRootArray(self, list_array):
        return array('d', list_array)
