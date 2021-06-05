import librosa

from Domain.Builder.IMusicMetricsBuilder import IMusicMetricsBuilder
from Domain.Builder.MetricsBuilder.Enum.Rhythm import Rhythm
from Domain.Builder.MetricsBuilder.Enum.Tempo import Tempo


class RhythmicMetricBuilder(IMusicMetricsBuilder):
    SLOW_RATE = 40
    ANDANTE_RATE = 65
    LIVELY_RATE = 100
    FAST_RATE = 170

    def __getAverageInterval(self, beatTimes):
        sumOfIntervals = 0
        for i in range(0, len(beatTimes) - 1):
            sumOfIntervals += beatTimes[i + 1] - beatTimes[i]
        return sumOfIntervals / (len(beatTimes) - 1)

    def __getRate(self, tempo):
        if tempo < self.SLOW_RATE:
            return Tempo.UNDEFINED
        if self.SLOW_RATE <= tempo < self.ANDANTE_RATE:
            return Tempo.SLOWLY
        if self.ANDANTE_RATE <= tempo < self.LIVELY_RATE:
            return Tempo.ANDANTE
        if self.LIVELY_RATE <= tempo < self.FAST_RATE:
            return Tempo.LIVELY
        if self.FAST_RATE <= tempo:
            return Tempo.FAST

    def buildPart(self, metrics, freq, amp=None):
        tempo, beatFrames = librosa.beat.beat_track(amp)
        beatTimes = librosa.frames_to_time(beatFrames)
        averageInterval = self.__getAverageInterval(beatTimes)
        if averageInterval > 1:
            metrics.setRhythm(Rhythm.SYNCOPE)
        else:
            metrics.setRhythm(Rhythm.DOTTED)
        metrics.setRate(self.__getRate(tempo))