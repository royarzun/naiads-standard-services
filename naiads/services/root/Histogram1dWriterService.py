# coding=utf-8

import json

from clara.base.ClaraUtils import ClaraUtils
from clara.engine.Engine import Engine
from clara.engine.EngineDataType import EngineDataType, Mimetype
from ROOT import TH1F

from naiads.utils.Utils import create_filename, convert_to_root_array, \
    get_limits


class Histogram1dWriterService(Engine):

    def __init__(self):
        pass

    def get_author(self):
        return "Ricardo Oyarzun <oyarzun@jlab.org>"

    def get_description(self):
        return "1D Histogram writer service, writes a ROOT file with Histogram"

    def get_states(self):
        pass

    def get_output_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.STRING())

    def execute(self, engine_data):
        if engine_data.mimetype == Mimetype.STRING:
            json_object = json.loads(engine_data.get_data())

            limits = get_limits(json_object["xAxis"]["centers"])
            histo_name = json_object["annotation"]["Title"]

            histo = TH1F("histogram", histo_name, 100, limits[0], limits[1])
            histo.SetContent(convert_to_root_array(json_object["counts"]))
            histo.SetError(convert_to_root_array(json_object["errors"]))

            histo.SaveAs(create_filename(histo_name))
            return engine_data

        return None

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