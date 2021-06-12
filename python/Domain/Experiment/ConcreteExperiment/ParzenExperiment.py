import numpy as np
import math
from sklearn.neighbors import KNeighborsClassifier
from Util.QualityUtil import QualityUtil
from Util.GraphUtil import GraphUtil
import json


class ParzenExperiment:
    __h = None
    __qualityUtil = None
    __graphUtil = None
    __kernel = None

    def __init__(self):
        self.__qualityUtil = QualityUtil()
        self.__graphUtil = GraphUtil()

    def setParams(self, params):
        h = params.get('h')
        if h is not None:
            self.__h = float(h)
        self.__kernel = params.get('kernel')

    def __PKernel(self, distance, h):
        ret = np.array(distance) / h
        return np.abs(ret) <= 1

    def __TKernel(self, distance, h):
        ret = np.array(distance) / h
        return (1 - np.abs(ret)) * (np.abs(ret) <= 1)

    def __EKernel(self, distance, h):
        ret = np.array(distance) / h
        return (1 - ret ** 2) * (np.abs(ret) <= 1)

    def __QKernel(self, distance, h):
        ret = np.array(distance) / h
        return ((1 - ret ** 2) ** 2) * (np.abs(ret) <= 1)

    # def __GKernel(self, distance, h):
    #     ret = np.array(distance) / h
    #     return math.exp(-2 * (ret ** 2))

    def __range(self, start, stop, step):
        current = start
        result = []
        while current <= stop:
            result.append(current)
            current += step
        return result

    def getResult(self, trainX, testX, trainY, testY):
        kernel = {
            'P': self.__PKernel,
            'T': self.__TKernel,
            'E': self.__EKernel,
            'Q': self.__QKernel,
            # 'G': self.__GKernel
        }
        if self.__kernel is not None and self.__h is not None:
            kernelFunc = kernel.get(self.__kernel)
            model = KNeighborsClassifier(n_neighbors=len(trainX), weights=lambda x: kernelFunc(x, self.__h))
            model.fit(trainX, trainY.values.ravel())
            predict = model.predict(testX)
            quality = self.__qualityUtil.getQuality(testY, predict)
            params = {
                'h': self.__h,
                'kernel': self.__kernel
            }
            result = {
                'params': params,
                'quality': quality
            }
            return json.dumps(result)
        elif self.__kernel is not None:
            experiments = {}
            for i, h in enumerate(self.__range(0.01, 2, 0.01)):
                kernelFunc = kernel.get(self.__kernel)
                model = KNeighborsClassifier(n_neighbors=len(trainX), weights=lambda x: kernelFunc(x, h))
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'h': h,
                    'kernel': self.__kernel
                }
                result = {
                    'params': params,
                    'quality': quality,
                    'train': model.score(trainX, trainY)
                }
                experiments[i] = result
            bestResult = self.__qualityUtil.getBestQualityExperiment(experiments)
            axis = self.__graphUtil.getAxis(experiments, 'h')
            graphs = {
                '0': self.__graphUtil.getGraph(
                    'Измение точности от h',
                    axis.get('Точность').get('x'),
                    axis.get('Точность').get('y'),
                    'h',
                    'Точность'
                ),
                '1': self.__graphUtil.getGraph(
                    'Измение полноты от h',
                    axis.get('Полнота').get('x'),
                    axis.get('Полнота').get('y'),
                    'h',
                    'Полнота'
                )
            }
            bestResult['graphs'] = graphs
            return json.dumps(bestResult)
        elif self.__h is not None:
            experiments = {}
            i = 0
            for name, func in kernel.items():
                model = KNeighborsClassifier(n_neighbors=len(trainX), weights=lambda x: func(x, self.__h))
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'h': self.__h,
                    'kernel': name
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
        allExperiments = {}
        k = 0
        graphs = {}
        for name, func in kernel.items():
            experiments = {}
            for i, h in enumerate(self.__range(0.01, 2, 0.01)):
                model = KNeighborsClassifier(n_neighbors=len(trainX), weights=lambda x: func(x, h))
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'h': h,
                    'kernel': name
                }
                result = {
                    'params': params,
                    'quality': quality,
                    'train': model.score(trainX, trainY)
                }
                experiments[i] = result
            allExperiments[k] = self.__qualityUtil.getBestQualityExperiment(experiments)
            axis = self.__graphUtil.getAxis(experiments, 'h')
            graphs[k * 2] = self.__graphUtil.getGraph(
                'Измение точности от h при функции ядра ' + name,
                axis.get('Точность').get('x'),
                axis.get('Точность').get('y'),
                'h',
                'Точность'
            )
            graphs[k * 2 + 1] = self.__graphUtil.getGraph(
                'Измение полноты от h при функции ядра ' + name,
                axis.get('Полнота').get('x'),
                axis.get('Полнота').get('y'),
                'h',
                'Полнота'
            )
            k += 1
        bestResult = self.__qualityUtil.getBestQualityExperiment(allExperiments)
        bestResult['graphs'] = graphs
        return json.dumps(bestResult)
