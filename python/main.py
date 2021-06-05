import librosa

from Domain.Builder.MusicMetricsBuilder import MusicMetricsBuilder

AMPLITUDE_NORMALIZE_COEFFICIENT = 30
FREQ_NORMALIZE_COEFFICIENT = 6
SIGNIFICANT_FREQ = 1


def getFreq(amp):
    result = []
    for i in range(0, amp.shape[1]):
        findingFreq = 0
        freqIndex = 0
        for j in range(0, amp.shape[0]):
            if amp[j, i] > SIGNIFICANT_FREQ:
                freqIndex = j
                findingFreq = amp[j, i]
        if findingFreq > SIGNIFICANT_FREQ:
            result.append(freqIndex * FREQ_NORMALIZE_COEFFICIENT)
        else:
            result.append(0)
    return result


audioData = 'test.wav'
builder = MusicMetricsBuilder()
beatFrames, sr = librosa.load(audioData)
XFrames = librosa.stft(beatFrames)
ampNormalizedForFreq = librosa.amplitude_to_db(abs(XFrames) * AMPLITUDE_NORMALIZE_COEFFICIENT)
builder.build(getFreq(ampNormalizedForFreq), beatFrames)
print(builder.getResult())
