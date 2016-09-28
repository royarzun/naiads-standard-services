# coding=utf-8

import json
import ROOT

from clara.engine.Engine import Engine
from clara.engine.EngineDataType import EngineDataType, Mimetype


class HistogramEngine(Engine):
    ONE_D_HISTOGRAM = "1D_HISTOGRAM"
    TWO_D_HISTOGRAM = "2D_HISTOGRAM"
    ONE_D_PROFILE = "1D_PROFILE"
    TWO_D_PROFILE = "2D_PROFILE"

    def __init__(self):
        self._h1f = None
        self._h2f = None
        self._p1f = None
        self._p2f = None

        self._h1f_label = None
        self._h1f_xbins = None
        self._h1f_xmin = None
        self._h1f_xmax = None

        self._p1f_label = None
        self._p1f_xbins = None
        self._p1f_xmin = None
        self._p1f_xmax = None

        self._h2f_label = None
        self._h2f_xbins = None
        self._h2f_xmin = None
        self._h2f_xmax = None
        self._h2f_ybins = None
        self._h2f_ymin = None
        self._h2f_ymax = None

        self._p2f_label = None
        self._p2f_xbins = None
        self._p2f_xmin = None
        self._p2f_xmax = None
        self._p2f_ybins = None
        self._p2f_ymin = None
        self._p2f_ymax = None

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
        if mt in [Mimetype.ARRAY_STRING, Mimetype.STRING]:
            try:
                ds_data = engine_data.get_data()
                if str(ds_data) in ["NEXT", "END_OF_DATA", "SKIP"]:
                    return engine_data
                else:
                    self._get_histogram(json.loads(str(ds_data)))

            except Exception as e:
                print "Received: " + engine_data.get_data()
                raise e

        return engine_data

    def configure(self, engine_data):
        config = engine_data.get_data()

        self._h1f_label = config[0]
        self._h1f_xbins = config[1]
        self._h1f_xmin = config[2]
        self._h1f_xmax = config[3]

        self._p1f_label = config[5]
        self._p1f_xbins = config[6]
        self._p1f_xmin = config[7]
        self._p1f_xmax = config[8]

        self._h2f_label = config[11]
        self._h2f_xbins = config[12]
        self._h2f_xmin = config[13]
        self._h2f_xmax = config[14]
        self._h2f_ybins = config[15]
        self._h2f_ymin = config[16]
        self._h2f_ymax = config[17]

        self._p2f_label = config[20]
        self._p2f_xbins = config[21]
        self._p2f_xmin = config[22]
        self._p2f_xmax = config[23]
        self._p2f_ybins = config[24]
        self._p2f_ymin = config[25]
        self._p2f_ymax = config[26]

        self._h1f = ROOT.TH1F(self._h1f_label, self._h1f_label,
                              int(self._h1f_xbins),
                              int(self._h1f_xmin), int(self._h1f_xmax))

        self._h2f = ROOT.TH2F(self._h2f_label, self._h2f_label,
                              int(self._h2f_xbins),
                              int(self._h2f_xmin), int(self._h2f_xmax),
                              int(self._h2f_ybins),
                              int(self._h2f_ymin), int(self._h2f_ymax))

        self._p1f = ROOT.TProfile(self._p1f_label, self._p1f_label,
                                  int(self._p1f_xbins),
                                  int(self._p1f_xmin), int(self._p1f_xmax))

        self._p2f = ROOT.TProfile2D(self._p2f_label, self._p2f_label,
                                    int(self._p2f_xbins),
                                    int(self._p2f_xmin), int(self._p2f_xmax),
                                    int(self._p2f_ybins),
                                    int(self._p2f_ymin), int(self._p2f_ymax))

        return engine_data

    def destroy(self):
        pass

    def reset(self):
        self._h1f.Reset()
        self._h2f.Reset()

    def get_version(self):
        return "v0.1"

    def get_author(self):
        return "Ricardo Oyarzun <oyarzun@jlab.org>"

    def get_output_data_types(self):
        return [EngineDataType.ARRAY_STRING(), EngineDataType.STRING()]

    def _get_histogram(self, json_data):
        if self.ONE_D_HISTOGRAM in json_data:
            for i in json_data[self.ONE_D_HISTOGRAM]:
                self._h1f.Fill(float(i))

        if self.TWO_D_HISTOGRAM in json_data:
            for d in json_data[self.TWO_D_HISTOGRAM]:
                self._h2f.Fill(float(d[0]), float(d[1]))

        if self.ONE_D_PROFILE in json_data:
            for d in json_data[self.ONE_D_PROFILE]:
                self._p1f.Fill(float(d[0]), float(d[1]))

        if self.TWO_D_PROFILE in json_data:
            for d in json_data[self.TWO_D_PROFILE]:
                self._p2f.Fill(float(d[0]), float(d[1]), float(d[2]))
        else:
            raise Exception("Not recognizable histogram type was found!")
