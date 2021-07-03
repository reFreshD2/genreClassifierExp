from sklearn.svm import SVC
from Util.QualityUtil import QualityUtil
from Util.GraphUtil import GraphUtil
import json


class SVCExperiment:
    C_RANGE_START = 1
    C_RANGE_END = 10
    C_RANGE_STEP = 0.1
    __qualityUtil = None
    __graphUtil = None
    __map = {
        0: 'linear',
        1: 'poly',
        2: 'rbf',
        3: 'sigmoid',
    }
    __C = None
    __kernel = None

    def __range(self, start, stop, step):
        current = start
        result = []
        while current <= stop:
            result.append(current)
            current += step
        return result

    def __init__(self):
        self.__qualityUtil = QualityUtil()
        self.__graphUtil = GraphUtil()

    def setParams(self, params):
        C = params.get('C')
        if C is not None:
            self.__C = float(C)
        self.__kernel = params.get('kernel')

    def getResult(self, trainX, testX, trainY, testY):
        if self.__kernel is not None and self.__C is not None:
            model = SVC(C=self.__C, kernel=self.__kernel)
            model.fit(trainX, trainY.values.ravel())
            predict = model.predict(testX)
            quality = self.__qualityUtil.getQuality(testY, predict)
            params = {
                'C': self.__C,
                'kernel': self.__kernel
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
        elif self.__kernel is not None:
            experiments = {}
            for i, C in enumerate(self.__range(self.C_RANGE_START, self.C_RANGE_END, self.C_RANGE_STEP)):
                model = SVC(C=C, kernel=self.__kernel)
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'C': C,
                    'kernel': self.__kernel
                }
                result = {
                    'params': params,
                    'quality': quality,
                    'train': model.score(trainX, trainY)
                }
                experiments[i] = result
            bestResult = self.__qualityUtil.getBestQualityExperiment(experiments)
            axis = self.__graphUtil.getAxis(experiments, 'C')
            qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
            graphs = {
                0: self.__graphUtil.getLinePlot('Измение точности от C - регулирующий параметр',
                                                axis.get('Точность').get('x'),
                                                axis.get('Точность').get('y'), 'Регулирующий параметр', 'Точность'),
                1: self.__graphUtil.getLinePlot('Измение полноты от C - регулирующий параметр',
                                                axis.get('Полнота').get('x'),
                                                axis.get('Полнота').get('y'), 'Регулирующий параметр', 'Полнота'),
                2: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                               qualityGraphAxis.get('Точность').get('x'),
                                               qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
                3: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                               qualityGraphAxis.get('Полнота').get('x'),
                                               qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
            }
            bestResult['graphs'] = graphs
            return json.dumps(bestResult)
        elif self.__C is not None:
            experiments = {}
            for i in range(0, len(self.__map)):
                model = SVC(C=self.__C, kernel=self.__map.get(i))
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'C': self.__C,
                    'kernel': self.__map.get(i)
                }
                result = {
                    'params': params,
                    'quality': quality,
                    'train': model.score(trainX, trainY)
                }
                experiments[i] = result
            bestResult = self.__qualityUtil.getBestQualityExperiment(experiments)
            axis = self.__graphUtil.getAxis(experiments, 'kernel')
            qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
            graphs = {
                0: self.__graphUtil.getBarPlot('Измение точности от kernel - функция ядра',
                                               axis.get('Точность').get('x'),
                                               axis.get('Точность').get('y'), 'Функция ядра', 'Точность'),
                1: self.__graphUtil.getBarPlot('Измение полноты от kernel - функция ядра',
                                               axis.get('Полнота').get('x'),
                                               axis.get('Полнота').get('y'), 'Функция ядра', 'Полнота'),
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
        for i in range(0, len(self.__map)):
            experiments = {}
            for j, C in enumerate(self.__range(self.C_RANGE_START, self.C_RANGE_END, self.C_RANGE_STEP)):
                model = SVC(C=C, kernel=self.__map.get(i))
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'C': C,
                    'kernel': self.__map.get(i)
                }
                result = {
                    'params': params,
                    'quality': quality,
                    'train': model.score(trainX, trainY)
                }
                experiments[j] = result
            bestExperiments[i] = self.__qualityUtil.getBestQualityExperiment(experiments)
            allExperiments[i] = experiments
        bestResult = self.__qualityUtil.getBestQualityExperiment(bestExperiments)
        bestKernel = bestResult.get('params').get('kernel')
        invertMap = {v: k for k, v in self.__map.items()}
        axis = self.__graphUtil.getAxis(allExperiments.get(invertMap.get(bestKernel)), 'C')
        qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
        graphs = {
            0: self.__graphUtil.getLinePlot(
                'Измение точности от С - регулирующий коэфициент, при функции ядра ' + bestKernel,
                axis.get('Точность').get('x'), axis.get('Точность').get('y'), 'Регулирующий коэфициент', 'Точность'),
            1: self.__graphUtil.getLinePlot(
                'Измение полноты от С - регулирующий коэфициент, при функции ядра ' + bestKernel,
                axis.get('Полнота').get('x'), axis.get('Полнота').get('y'), 'Регулирующий коэфициент', 'Полнота'),
            2: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                           qualityGraphAxis.get('Точность').get('x'),
                                           qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
            3: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                           qualityGraphAxis.get('Полнота').get('x'),
                                           qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
        }
        bestResult['graphs'] = graphs
        return json.dumps(bestResult)
