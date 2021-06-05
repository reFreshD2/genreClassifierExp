from Domain.Builder.IMusicMetricsBuilder import IMusicMetricsBuilder
from Domain.Builder.MetricsBuilder.DTO.FreqUsingDTO import FreqUsingDTO


class MusicInstrumentsBuilder(IMusicMetricsBuilder):
    SIGNIFICANT_COUNT_FREQ = 3

    def __getFreq(self, container, finding):
        for i in range(0, len(container)):
            if container[i].getFreq() == finding:
                return container[i]
        return None

    def __getFreqUsing(self, freq):
        result = []
        for i in range(0, len(freq)):
            freqUsing = self.__getFreq(result, freq[i])
            if freqUsing is not None:
                freqUsing.inc()
            else:
                result.append(FreqUsingDTO(freq[i], 1))
        return result

    def __round(self, freq):
        result = []
        for i in range(0, len(freq)):
            result.append(round(freq[i], -1))
        return result

    def __filter(self, freq):
        result = []
        for i in range(0, len(freq)):
            if freq[i].getCount() >= self.SIGNIFICANT_COUNT_FREQ:
                result.append(freq[i])
        return result

    def buildPart(self, metrics, freq, amp=None):
        freqUsing = self.__getFreqUsing(self.__round(freq))
        filterFreqUsing = self.__filter(freqUsing)
        for i in range(0, len(filterFreqUsing)):
            print(filterFreqUsing[i].getFreq(), filterFreqUsing[i].getCount())
