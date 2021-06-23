from sklearn.linear_model import SGDClassifier
from Util.QualityUtil import QualityUtil
from Util.GraphUtil import GraphUtil
import json


class SGDExperiment:
    __qualityUtil = None
    __graphUtil = None
    __mapLoss = {
        0: 'hinge',
        1: 'log',
        2: 'modified_huber',
        3: 'squared_hinge',
        4: 'perceptron'
    }
    __mapPenalty = {
        0: 'l2',
        1: 'l1',
        2: 'elasticnet'
    }
    __loss = None
    __penalty = None

    def __init__(self):
        self.__qualityUtil = QualityUtil()
        self.__graphUtil = GraphUtil()

    def setParams(self, params):
        self.__loss = params.get('loss')
        self.__penalty = params.get('penalty')

    def getResult(self, trainX, testX, trainY, testY):
        if self.__loss is not None and self.__penalty is not None:
            model = SGDClassifier(loss=self.__loss, penalty=self.__penalty)
            model.fit(trainX, trainY.values.ravel())
            predict = model.predict(testX)
            quality = self.__qualityUtil.getQuality(testY, predict)
            params = {
                'loss': self.__loss,
                'penalty': self.__penalty
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
        elif self.__loss is not None:
            experiments = {}
            for i in range(0, len(self.__mapPenalty)):
                model = SGDClassifier(loss=self.__loss, penalty=self.__mapPenalty.get(i))
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'loss': self.__loss,
                    'penalty': self.__mapPenalty.get(i)
                }
                result = {
                    'params': params,
                    'quality': quality,
                    'train': model.score(trainX, trainY)
                }
                experiments[i] = result
            bestResult = self.__qualityUtil.getBestQualityExperiment(experiments)
            axis = self.__graphUtil.getAxis(experiments, 'penalty')
            qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
            graphs = {
                0: self.__graphUtil.getLinePlot('Измение точности от penalty - функции штрафа',
                                                axis.get('Точность').get('x'),
                                                axis.get('Точность').get('y'), 'Функция штрафа', 'Точность'),
                1: self.__graphUtil.getLinePlot('Измение полноты от penalty - функции штрафа',
                                                axis.get('Полнота').get('x'),
                                                axis.get('Полнота').get('y'), 'Функция штрафа', 'Полнота'),
                2: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                               qualityGraphAxis.get('Точность').get('x'),
                                               qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
                3: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                               qualityGraphAxis.get('Полнота').get('x'),
                                               qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
            }
            bestResult['graphs'] = graphs
            return json.dumps(bestResult)
        elif self.__penalty is not None:
            experiments = {}
            for i in range(0, len(self.__mapLoss)):
                model = SGDClassifier(loss=self.__mapLoss.get(i), penalty=self.__penalty)
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'loss': self.__mapLoss.get(i),
                    'kernel': self.__penalty
                }
                result = {
                    'params': params,
                    'quality': quality,
                    'train': model.score(trainX, trainY)
                }
                experiments[i] = result
            bestResult = self.__qualityUtil.getBestQualityExperiment(experiments)
            axis = self.__graphUtil.getAxis(experiments, 'loss')
            qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
            graphs = {
                0: self.__graphUtil.getBarPlot('Измение точности от loss - функции потерь',
                                               axis.get('Точность').get('x'),
                                               axis.get('Точность').get('y'), 'Функция потерь', 'Точность'),
                1: self.__graphUtil.getBarPlot('Измение полноты от loss - функции потерь',
                                               axis.get('Полнота').get('x'),
                                               axis.get('Полнота').get('y'), 'Функция потерь', 'Полнота'),
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
        for i in range(0, len(self.__mapPenalty)):
            experiments = {}
            for j in range(0, len(self.__mapLoss)):
                model = SGDClassifier(loss=self.__mapLoss.get(j), penalty=self.__mapPenalty.get(i))
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'loss': self.__mapLoss.get(j),
                    'penalty': self.__mapPenalty.get(i)
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
        bestPenalty = bestResult.get('params').get('penalty')
        invertMap = {v: k for k, v in self.__mapPenalty.items()}
        axis = self.__graphUtil.getAxis(allExperiments.get(invertMap.get(bestPenalty)), 'loss')
        qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
        graphs = {
            0: self.__graphUtil.getLinePlot(
                'Измение точности от loss - функции потерь, при функции штрафа ' + bestPenalty,
                axis.get('Точность').get('x'), axis.get('Точность').get('y'), 'Функция потерь', 'Точность'),
            1: self.__graphUtil.getLinePlot(
                'Измение полноты от loss - функции потерь, при функции штрафа ' + bestPenalty,
                axis.get('Полнота').get('x'), axis.get('Полнота').get('y'), 'Функция потерь', 'Полнота'),
            2: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                           qualityGraphAxis.get('Точность').get('x'),
                                           qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
            3: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                           qualityGraphAxis.get('Полнота').get('x'),
                                           qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
        }
        bestResult['graphs'] = graphs
        return json.dumps(bestResult)
