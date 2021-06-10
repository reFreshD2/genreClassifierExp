from sklearn.neighbors import KNeighborsClassifier
from Util.QualityUtil import QualityUtil
import json


class KNeighborsExperiment:
    __k = None
    __qualityUtil = None

    def __init__(self):
        self.__qualityUtil = QualityUtil()

    def setParams(self, params):
        try:
            self.__k = int(params.get('k'))
        except KeyError as e:
            self.__k = None

    def getResult(self, trainX, testX, trainY, testY):
        if self.__k is not None:
            model = KNeighborsClassifier(n_neighbors=self.__k)
            model.fit(trainX, trainY)
            predict = model.predict(testX)
            quality = self.__qualityUtil.getQuality(testY, predict)
            params = {
                'k': self.__k
            }
            result = {
                'params': params,
                'quality': quality
            }
            return json.dumps(result)
