from Domain.Entity.MusicMetrics import MusicMetrics
from Domain.Builder.MetricsBuilder.SpectroMetricBuilder import SpectroMetricBuilder
from Domain.Builder.MetricsBuilder.RhythmicMetricBuilder import RhythmicMetricBuilder
from Domain.Builder.MetricsBuilder.MusicInstrumentsBuilder import MusicInstrumentsBuilder
from Domain.Builder.MetricsBuilder.SceptrogramBuilder import SpectrogramBuilder
from Domain.Builder.MetricsBuilder.MusicFormBuilder import MusicFormBuilder
import json


class MusicMetricsBuilder:
    __builders = [
        SpectroMetricBuilder(),
        RhythmicMetricBuilder(),
        MusicInstrumentsBuilder(),
        SpectrogramBuilder(),
        MusicFormBuilder()
    ]

    def __init__(self):
        self.__musicMetrics = MusicMetrics()

    def build(self, freq, apm):
        for i in range(0, len(self.__builders)):
            self.__builders[i].buildPart(self.__musicMetrics, freq, apm)

    def getResult(self):
        return json.dumps(self.__musicMetrics, default=lambda o: self.__musicMetrics.__dict__)
