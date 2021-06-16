import random

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from Util.QualityUtil import QualityUtil
from Util.GraphUtil import GraphUtil
import json


class KNeighborsWeightExperiment:
    __k = None
    __qualityUtil = None
    __graphUtil = None
    __weight = None
    __map = {
        0: 'linear',
        1: 'exp'
    }

    def __init__(self):
        self.__qualityUtil = QualityUtil()
        self.__graphUtil = GraphUtil()

    def setParams(self, params):
        k = params.get('k')
        if k is not None:
            self.__k = int(k)
        self.__weight = params.get('weight')

    def __linear(self, distance):
        ret = np.ones_like(distance)
        k = ret.shape[1]
        for i in range(k):
            ret[:, i] *= (k + 1 - i) / k
        return ret

    def __exp(self, distance):
        ret = np.ones_like(distance)
        k = ret.shape[1]
        q = random.uniform(0, 1)
        for i in range(k):
            ret[:, i] *= q ** i
        return ret

    def getResult(self, trainX, testX, trainY, testY):
        if self.__weight is not None and self.__k is not None:
            if self.__weight == 'linear':
                model = KNeighborsClassifier(n_neighbors=self.__k, weights=self.__linear)
            else:
                model = KNeighborsClassifier(n_neighbors=self.__k, weights=self.__exp)
            model.fit(trainX, trainY.values.ravel())
            predict = model.predict(testX)
            quality = self.__qualityUtil.getQuality(testY, predict)
            params = {
                'k': self.__k,
                'weight': self.__weight
            }
            result = {
                'params': params,
                'quality': quality,
                'test': model.score(trainX, trainY)
            }
            qualityGraphAxis = self.__graphUtil.getQualityByGenre(quality)
            graphs = {
                0: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                               qualityGraphAxis.get('Точность').get('x'),
                                               qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
                1: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                               qualityGraphAxis.get('Полнота').get('x'),
                                               qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
            }
            result['graphs'] = graphs
            return json.dumps(result)
        elif self.__weight is not None:
            experiments = {}
            for i in range(1, len(trainX)):
                if self.__weight == 'linear':
                    model = KNeighborsClassifier(n_neighbors=i, weights=self.__linear)
                else:
                    model = KNeighborsClassifier(n_neighbors=i, weights=self.__exp)
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'k': i,
                    'weight': self.__weight
                }
                result = {
                    'params': params,
                    'quality': quality,
                    'train': model.score(trainX, trainY)
                }
                experiments[i - 1] = result
            bestResult = self.__qualityUtil.getBestQualityExperiment(experiments)
            axis = self.__graphUtil.getAxis(experiments, 'k')
            qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
            graphs = {
                0: self.__graphUtil.getLinePlot('Измение точности от k - количество соседей',
                                                axis.get('Точность').get('x'),
                                                axis.get('Точность').get('y'), 'Количество соседей', 'Точность'),
                1: self.__graphUtil.getLinePlot('Измение полноты от k - количество соседей',
                                                axis.get('Полнота').get('x'),
                                                axis.get('Полнота').get('y'), 'k', 'Полнота'),
                2: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                               qualityGraphAxis.get('Точность').get('x'),
                                               qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
                3: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                               qualityGraphAxis.get('Полнота').get('x'),
                                               qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
            }
            bestResult['graphs'] = graphs
            return json.dumps(bestResult)
        elif self.__k is not None:
            experiments = {}
            weightFunc = {
                'linear': self.__linear,
                'exp': self.__exp
            }
            i = 0
            for name, func in weightFunc.items():
                model = KNeighborsClassifier(n_neighbors=self.__k, weights=func)
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'k': self.__k,
                    'weight': name
                }
                result = {
                    'params': params,
                    'quality': quality,
                    'train': model.score(trainX, trainY)
                }
                experiments[i] = result
                i += 1
            bestResult = self.__qualityUtil.getBestQualityExperiment(experiments)
            axis = self.__graphUtil.getAxis(experiments, 'weight')
            qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
            graphs = {
                0: self.__graphUtil.getBarPlot('Измение точности от weight - функция весов',
                                               axis.get('Точность').get('x'),
                                               axis.get('Точность').get('y'), 'Функция весов', 'Точность'),
                1: self.__graphUtil.getBarPlot('Измение полноты от weight - функция весов',
                                               axis.get('Полнота').get('x'),
                                               axis.get('Полнота').get('y'), 'Функция весов', 'Полнота'),
                2: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                               qualityGraphAxis.get('Точность').get('x'),
                                               qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
                3: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                               qualityGraphAxis.get('Полнота').get('x'),
                                               qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
            }
            bestResult['graphs'] = graphs
            return json.dumps(bestResult)
        weightFunc = {
            'linear': self.__linear,
            'exp': self.__exp
        }
        allExperiments = {}
        bestExperiments = {}
        k = 0
        for name, func in weightFunc.items():
            experiments = {}
            for i in range(1, len(trainX)):
                model = KNeighborsClassifier(n_neighbors=i, weights=func)
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'k': i,
                    'weight': name
                }
                result = {
                    'params': params,
                    'quality': quality,
                    'train': model.score(trainX, trainY)
                }
                experiments[i - 1] = result
            bestExperiments[k] = self.__qualityUtil.getBestQualityExperiment(experiments)
            allExperiments[k] = experiments
            k += 1
        bestResult = self.__qualityUtil.getBestQualityExperiment(bestExperiments)
        bestWeight = bestResult.get('params').get('weight')
        invertMap = {v: k for k, v in self.__map.items()}
        axis = self.__graphUtil.getAxis(allExperiments.get(invertMap.get(bestWeight)), 'k')
        qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
        graphs = {
            0: self.__graphUtil.getLinePlot(
                'Измение точности от k - количество соседей, при функции весов ' + bestWeight,
                axis.get('Точность').get('x'), axis.get('Точность').get('y'), 'Количество соседей', 'Точность'),
            1: self.__graphUtil.getLinePlot(
                'Измение полноты от k - количество соседей, при функции весов ' + bestWeight,
                axis.get('Полнота').get('x'), axis.get('Полнота').get('y'), 'Количество соседей', 'Полнота'),
            2: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                           qualityGraphAxis.get('Точность').get('x'),
                                           qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
            3: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                           qualityGraphAxis.get('Полнота').get('x'),
                                           qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
        }
        bestResult['graphs'] = graphs
        return json.dumps(bestResult)
