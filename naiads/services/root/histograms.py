# coding=utf-8

import ROOT

# from naiads.utils.Utils import create_filename


def create_1d_histogram(json_object):
    histogram = ROOT.TH1F("1D_HISTOGRAM", "1D_HISTOGRAM", 100, 0, 10000)
    for i in json_object["1D_HISTOGRAM"]:
        histogram.Fill(float(i))
    buf = ROOT.TBufferFile(ROOT.TBuffer.kWrite)
    buf.Reset()
    if not buf.WriteObjectAny(histogram, ROOT.TH1F.Class()):
        print "failed"
        return 1
    return buf.Buffer()
    # histogram.SaveAs(create_filename(output_dir, "1D_HISTOS"))


def create_2d_histogram(json_object):
    histogram = ROOT.TH2F("2D_HISTOGRAM", "2D_HISTOGRAM", 100, 0, 18000, 100, 0, 10000)

    for d in json_object["2D_HISTOGRAM"]:
        for i, j in d:
            histogram.Fill(float(i), float(j))
    buf = ROOT.TBufferFile(ROOT.TBuffer.kWrite)
    buf.Reset()
    if not buf.WriteObjectAny(histogram, ROOT.TH1F.Class()):
        print "failed"
        return 1
    return buf
    # histogram.SaveAs(create_filename(output_dir, "2D_HISTOS"))
