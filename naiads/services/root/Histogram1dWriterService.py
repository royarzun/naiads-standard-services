# coding=utf-8

import json

from clara.base.ClaraUtils import ClaraUtils
from clara.engine.Engine import Engine
from clara.engine.EngineStatus import EngineStatus
from clara.engine.EngineDataType import EngineDataType, Mimetype

from naiads.services.root.histograms import create_1d_histogram
from naiads.utils.Utils import set_output_folder


class Histogram1dWriterService(Engine):

    def __init__(self):
        self.output_dir = "./"

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
            create_1d_histogram(json.loads(engine_data.get_data()),
                                self.output_dir)
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
        if engine_data.mimetype == Mimetype.STRING():
            json_object = json.loads(engine_data.get_data())
            try:
                self.output_dir = set_output_folder(json_object['output_dir'])
                return engine_data

            except IOError as e:
                engine_data.status(EngineStatus.ERROR)
                engine_data.description(e.message)
                return engine_data

        return engine_data
