class FreqUsingDTO:
    __freq = None
    __count = 0

    def __init__(self, freq, count):
        self.__freq = freq
        self.__count = count

    def getFreq(self):
        return self.__freq

    def getCount(self):
        return self.__count

    def inc(self):
        self.__count += 1
