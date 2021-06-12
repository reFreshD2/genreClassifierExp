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
                'quality': quality
            }
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
            return json.dumps(bestResult)
        weightFunc = {
            'linear': self.__linear,
            'exp': self.__exp
        }
        allExperiments = {}
        k = 0
        graphs = {}
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
            allExperiments[k] = self.__qualityUtil.getBestQualityExperiment(experiments)
            axis = self.__graphUtil.getAxis(experiments, 'k')
            graphs[k * 2] = self.__graphUtil.getGraph(
                'Измение точности от k при функции весов ' + name,
                axis.get('Точность').get('x'),
                axis.get('Точность').get('y'),
                'k',
                'Точность'
            )
            graphs[k * 2 + 1] = self.__graphUtil.getGraph(
                'Измение полноты от k при функции весов ' + name,
                axis.get('Полнота').get('x'),
                axis.get('Полнота').get('y'),
                'k',
                'Полнота'
            )
            k += 1
        bestResult = self.__qualityUtil.getBestQualityExperiment(allExperiments)
        bestResult['graphs'] = graphs
        return json.dumps(bestResult)
