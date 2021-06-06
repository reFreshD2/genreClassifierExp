from Domain.Builder.IMusicMetricsBuilder import IMusicMetricsBuilder
from Domain.Builder.MetricsBuilder.DTO.FreqUsingDTO import FreqUsingDTO


class MusicInstrumentsSoundCharacterBuilder(IMusicMetricsBuilder):
    SOUND_CHARACTER = {
        'BUZZ': [20, 30],
        'BOTTOM': [60, 80],
        'FULLNESS': [80, 120],
        'TURBIDITY': [120, 200],
        'HEAT': [200, 400],
        'DENSITY': [500, 900],
        'SONORITY': [1000, 2000],
        'CLARITY': [2000, 2500],
        'PRESENCE': [2500, 5000],
        'SHARPNESS': [5000, 7500],
        'HISS': [8000, 12000]
    }

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

    def __getInstumentsSoundCharacter(self, freqUsing):
        result = {}
        sumCount = 0
        for i in range(0, len(freqUsing)):
            sumCount += freqUsing[i].getCount()
        for i in range(0, len(self.SOUND_CHARACTER)):
            sumFreq = 0
            key = list(self.SOUND_CHARACTER.keys())[i]
            for j in range(0, len(freqUsing)):
                if self.SOUND_CHARACTER.get(key)[0] <= freqUsing[j].getFreq() <= self.SOUND_CHARACTER.get(key)[1]:
                    sumFreq += freqUsing[j].getCount()
            result[key] = round(sumFreq / sumCount, 4)
        return result

    def buildPart(self, metrics, freq, amp=None):
        freqUsing = self.__getFreqUsing(self.__round(freq))
        metrics.setInstumentsSoundCharacter(self.__getInstumentsSoundCharacter(freqUsing))
