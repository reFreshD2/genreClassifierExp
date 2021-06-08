import librosa

from Domain.Builder.MusicMetricsBuilder import MusicMetricsBuilder


class Parser:
    AMPLITUDE_NORMALIZE_COEFFICIENT = 30
    FREQ_NORMALIZE_COEFFICIENT = 6
    SIGNIFICANT_FREQ = 1
    __builder = None

    def __init__(self):
        self.__builder = MusicMetricsBuilder()

    def __getFreq(self, amp):
        result = []
        for i in range(0, amp.shape[1]):
            findingFreq = 0
            freqIndex = 0
            for j in range(0, amp.shape[0]):
                if amp[j, i] > self.SIGNIFICANT_FREQ:
                    freqIndex = j
                    findingFreq = amp[j, i]
            if findingFreq > self.SIGNIFICANT_FREQ:
                result.append(freqIndex * self.FREQ_NORMALIZE_COEFFICIENT)
            else:
                result.append(0)
        return result

    def parse(self, audioData):
        beatFrames, sr = librosa.load(audioData)
        XFrames = librosa.stft(beatFrames)
        ampNormalizedForFreq = librosa.amplitude_to_db(abs(XFrames) * self.AMPLITUDE_NORMALIZE_COEFFICIENT)
        self.__builder.build(self.__getFreq(ampNormalizedForFreq), beatFrames)
        return self.__builder.getResult()
