from sklearn.neighbors import KNeighborsClassifier
from Util.QualityUtil import QualityUtil
from Util.GraphUtil import GraphUtil
import json


class KNeighborsExperiment:
    __k = None
    __qualityUtil = None
    __graphUtil = None

    def __getAxis(self, experiments):
        x = []
        yPrecision = []
        yRecall = []
        for i in range(0, len(experiments)):
            x.append(experiments.get(i).get('params').get('k'))
            yPrecision.append(experiments.get(i).get('quality').get('Средняя точность'))
            yRecall.append(experiments.get(i).get('quality').get('Средняя полнота'))
        return {
            'Точность': {
                'x': x,
                'y': yPrecision
            },
            'Полнота': {
                'x': x,
                'y': yRecall
            }
        }

    def __init__(self):
        self.__qualityUtil = QualityUtil()
        self.__graphUtil = GraphUtil()

    def setParams(self, params):
        try:
            param = params.get('k')
            if param is not None:
                self.__k = int(param)
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
        experiments = {}
        for i in range(1, len(trainX)):
            model = KNeighborsClassifier(n_neighbors=i)
            model.fit(trainX, trainY.values.ravel())
            predict = model.predict(testX)
            quality = self.__qualityUtil.getQuality(testY, predict)
            params = {
                'k': i
            }
            result = {
                'params': params,
                'quality': quality,
                'train': model.score(trainX, trainY)
            }
            experiments[i-1] = result
        bestResult = self.__qualityUtil.getBestQualityExperiment(experiments)
        axis = self.__getAxis(experiments)
        graphs = {
            '0': self.__graphUtil.getGraph(
                'Измение точности от k',
                axis.get('Точность').get('x'),
                axis.get('Точность').get('y'),
                'k',
                'Точность'
            ),
            '1': self.__graphUtil.getGraph(
                'Измение полноты от k',
                axis.get('Полнота').get('x'),
                axis.get('Полнота').get('y'),
                'k',
                'Полнота'
            )
        }
        bestResult['graphs'] = graphs
        return json.dumps(bestResult)
