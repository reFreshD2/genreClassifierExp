import numpy as np
import math
from sklearn.neighbors import KNeighborsClassifier
from Util.QualityUtil import QualityUtil
from Util.GraphUtil import GraphUtil
import json


class ParzenExperiment:
    H_RANGE_START = 0.01
    H_RANGE_END = 2
    H_RANGE_STEP = 0.01
    __h = None
    __qualityUtil = None
    __graphUtil = None
    __kernel = None
    __map = {
        0: 'P',
        1: 'T',
        2: 'E',
        3: 'Q',
    }

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
                'quality': quality,
                'train': model.score(trainX, trainY)
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
        elif self.__kernel is not None:
            experiments = {}
            for i, h in enumerate(self.__range(self.H_RANGE_START, self.H_RANGE_END, self.H_RANGE_STEP)):
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
            qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
            graphs = {
                0: self.__graphUtil.getLinePlot('Измение точности от h - ширина окна', axis.get('Точность').get('x'),
                                                axis.get('Точность').get('y'), 'Ширина окна', 'Точность'),
                1: self.__graphUtil.getLinePlot('Измение полноты от h', axis.get('Полнота').get('x'),
                                                axis.get('Полнота').get('y'), 'Ширина окна', 'Полнота'),
                2: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                               qualityGraphAxis.get('Точность').get('x'),
                                               qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
                3: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                               qualityGraphAxis.get('Полнота').get('x'),
                                               qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
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
            axis = self.__graphUtil.getAxis(experiments, 'kernel')
            qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
            graphs = {
                0: self.__graphUtil.getBarPlot('Изменение точности от ядра', axis.get('Точность').get('x'),
                                               axis.get('Точность').get('y'), 'Ядро', 'Точность'),
                1: self.__graphUtil.getBarPlot('Изменение полноты от ядра', axis.get('Полнота').get('x'),
                                               axis.get('Точность').get('y'), 'Ядро', 'Полнота'),
                2: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                               qualityGraphAxis.get('Точность').get('x'),
                                               qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
                3: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                               qualityGraphAxis.get('Полнота').get('x'),
                                               qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
            }
            bestResult['graphs'] = graphs
            return json.dumps(bestResult)
        allExperiments = {}
        bestExperiments = {}
        k = 0
        for name, func in kernel.items():
            experiments = {}
            for i, h in enumerate(self.__range(self.H_RANGE_START, self.H_RANGE_END, self.H_RANGE_STEP)):
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
            bestExperiments[k] = self.__qualityUtil.getBestQualityExperiment(experiments)
            allExperiments[k] = experiments
            k += 1
        bestResult = self.__qualityUtil.getBestQualityExperiment(bestExperiments)
        bestKernel = bestResult.get('params').get('kernel')
        invertMap = {v: k for k, v in self.__map.items()}
        axis = self.__graphUtil.getAxis(allExperiments.get(invertMap.get(bestKernel)), 'h')
        qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
        graphs = {
            0: self.__graphUtil.getLinePlot('Измение точности от h - ширина окна, при функции ядра ' + bestKernel,
                                            axis.get('Точность').get('x'), axis.get('Точность').get('y'), 'Ширина окна',
                                            'Точность'),
            1: self.__graphUtil.getLinePlot('Измение полноты от h - ширина окна, при функции ядра ' + bestKernel,
                                            axis.get('Полнота').get('x'), axis.get('Полнота').get('y'), 'Ширина окна',
                                            'Полнота'),
            2: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                           qualityGraphAxis.get('Точность').get('x'),
                                           qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
            3: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                           qualityGraphAxis.get('Полнота').get('x'),
                                           qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
        }
        bestResult['graphs'] = graphs
        return json.dumps(bestResult)
