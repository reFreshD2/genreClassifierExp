class MusicMetrics:

    def __init__(self):
        self.__minFreq = None
        self.__avgFreq = None
        self.__maxFreq = None
        self.__minAmp = None
        self.__maxAmp = None
        self.__avgAmp = None
        self.__rhythm = None
        self.__rate = None
        self.__instruments = []
        self.__musicForm = None
        self.__genre = None
        self.__spectralCentroid = None
        self.__spectralRollOf = None
        self.__spectralBandWidth = None

    def setMinFreq(self, value):
        self.__minFreq = value

    def setMaxFreq(self, value):
        self.__maxFreq = value

    def setAvgFreq(self, value):
        self.__avgFreq = value

    def setMinAmp(self, value):
        self.__minAmp = value

    def setMaxAmp(self, value):
        self.__maxAmp = value

    def setAvgAmp(self, value):
        self.__avgAmp = value

    def setRhythm(self, value):
        self.__rhythm = value

    def setRate(self, value):
        self.__rate = value

    def setSpectralCentroid(self, value):
        self.__spectralCentroid = value

    def setSpectralRollOff(self, value):
        self.__spectralRollOf = value

    def setSpectralBandWidth(self, value):
        self.__spectralBandWidth = value

    def setForm(self, value):
        self.__musicForm = value
