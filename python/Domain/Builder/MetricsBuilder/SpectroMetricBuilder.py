import numpy

from Domain.Builder.IMusicMetricsBuilder import IMusicMetricsBuilder


class SpectroMetricBuilder(IMusicMetricsBuilder):
    SIGNIFICANT_AMPLITUDE = 0.0001

    def buildPart(self, metrics, freq, amp=None):
        maxFreq = 0
        minFreq = 42000
        sumFreq = 0

        for i in range(0, len(freq)):
            if freq[i] > maxFreq:
                maxFreq = freq[i]
            if minFreq > freq[i] > 0:
                minFreq = freq[i]
            sumFreq += freq[i]
        avgFreq = sumFreq / len(freq)

        maxAmp = 0
        minAmp = 1
        sumAmp = 0

        for i in range(0, len(amp)):
            if abs(amp[i]) > maxAmp:
                maxAmp = amp[i]
            if minAmp > abs(amp[i]) > self.SIGNIFICANT_AMPLITUDE:
                minAmp = abs(amp[i])
            sumAmp += abs(amp[i])
        avgAmp = sumAmp / len(amp)

        metrics.setMinFreq(minFreq)
        metrics.setMaxFreq(maxFreq)
        metrics.setAvgFreq(round(avgFreq, 4))
        metrics.setMinAmp(round(numpy.float(minAmp), 4))
        metrics.setMaxAmp(round(numpy.float(maxAmp), 4))
        metrics.setAvgAmp(round(avgAmp, 4))
