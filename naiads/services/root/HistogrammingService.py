# coding=utf-8

import json

from clara.engine.Engine import Engine
from clara.engine.EngineData import EngineData
from clara.engine.EngineDataType import EngineDataType, Mimetype

from naiads.services.root.histograms import create_1d_histogram,\
    create_2d_histogram


class HistogrammingService(Engine):
    ONE_D_HISTOGRAM = "1D_HISTOGRAM"
    TWO_D_HISTOGRAM = "2D_HISTOGRAM"
    ONE_D_PROFILE = "1D_PROFILE"
    TWO_D_PROFILE = "2D_PROFILE"

    def __init__(self):
        self.output_dir = "/ramdisk/out/"

    def execute_group(self, inputs):
        pass

    def get_description(self):
        return "Histogramming service for NAIADS stats. It creates on demand" \
               " the right type of Histogram based on the json description"

    def get_input_data_types(self):
        return [EngineDataType.ARRAY_STRING(), EngineDataType.STRING()]

    def get_states(self):
        pass

    def execute(self, engine_data):
        mt = engine_data.mimetype
        s_histogram = ""
        if mt in [Mimetype.ARRAY_STRING, Mimetype.STRING]:
            try:
                ds_data = engine_data.get_data()
                if str(ds_data) in ["NEXT", "END_OF_DATA", "SKIP"]:
                    return engine_data
                else:
                    s_histogram = self._get_histogram(json.loads(str(ds_data)))
            except Exception as e:
                print str(engine_data.get_data())
                raise e

        return engine_data.set_data(s_histogram, EngineDataType.STRING())

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
        return [EngineDataType.ARRAY_STRING(), EngineDataType.STRING()]

    def _get_histogram(self, json_data):

        if self.ONE_D_HISTOGRAM in json_data:
            create_1d_histogram(json_data)
        elif self.TWO_D_HISTOGRAM in json_data:
            create_2d_histogram(json_data)
        elif self.ONE_D_PROFILE in json_data:
            pass
        elif self.TWO_D_PROFILE in json_data:
            pass
        else:
            raise Exception("Not recognizable histogram type was found!")
