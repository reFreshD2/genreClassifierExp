import librosa
from Domain.Builder.IMusicMetricsBuilder import IMusicMetricsBuilder


class SpectrogramBuilder(IMusicMetricsBuilder):

    def __getAverage(self, array):
        summary = 0
        for i in range(0, len(array)):
            summary += array[i]
        return summary / len(array)

    def buildPart(self, metrics, freq, amp=None):
        spectralCentroids = librosa.feature.spectral_centroid(amp)[0]
        spectralRollOffs = librosa.feature.spectral_rolloff(amp + 0.01)[0]
        spectralBandWidth = librosa.feature.spectral_bandwidth(amp + 0.01)[0]

        metrics.setSpectralCentroid(self.__getAverage(spectralCentroids))
        metrics.setSpectralRollOff(self.__getAverage(spectralRollOffs))
        metrics.setSpectralBandWidth(self.__getAverage(spectralBandWidth))
