# coding=utf-8

import json

from clara.base.ClaraUtils import ClaraUtils
from clara.engine.Engine import Engine
from clara.engine.EngineDataType import EngineDataType, Mimetype
from clara.engine.EngineStatus import EngineStatus

from naiads.services.root.histograms import create_1d_histogram,\
    create_2d_histogram


class HistogrammingService(Engine):
    ONE_D_HISTOGRAM = "1D Histogram"
    TWO_D_HISTOGRAM = "2D Histogram"
    ONE_D_PROFILE = "1D Profile"
    TWO_D_PROFILE = "2D Profile"

    def __init__(self):
        self.output_dir = "./"

    def execute_group(self, inputs):
        pass

    def get_description(self):
        return "Histogramming service for NAIADS stats. It creates on demand " \
               "the right type of Histogram based on the json description"

    def get_input_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.JSON())

    def get_states(self):
        pass

    def execute(self, engine_data):
        if engine_data.mimetype == Mimetype.JSON:
            try:
                json_object = json.loads(engine_data.get_data())
                # First, lets identify what we are dealing with
                self._get_histogram(json_object)
            except Exception as e:
                engine_data.status(EngineStatus.ERROR)
                engine_data.description(e.message)
                return engine_data
            return engine_data

    def configure(self, engine_data):
        pass

    def destroy(self):
        pass

    def reset(self):
        pass

    def get_version(self):
        return "v0.1"

    def get_author(self):
        return "Ricardo Oyarzun <oyarzun@jlab.org>"

    def get_output_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.JSON())

    def _get_histogram(self, json_data):
        histogram_type = json_data["annotation"]["AidaPath"]

        if histogram_type.find(self.ONE_D_HISTOGRAM) == 0:
            create_1d_histogram(json_data, self.output_dir)
        elif histogram_type.find(self.TWO_D_HISTOGRAM) == 0:
            create_2d_histogram(json_data, self.output_dir)
        elif histogram_type.find(self.ONE_D_PROFILE) == 0:
            pass
        elif histogram_type.find(self.TWO_D_PROFILE) == 0:
            pass
        else:
            raise Exception("Not recognizable histogram type was found!")
