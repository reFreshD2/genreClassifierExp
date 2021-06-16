from sklearn.tree import DecisionTreeClassifier
from Util.QualityUtil import QualityUtil
from Util.GraphUtil import GraphUtil
import json


class DecisionTreeExperiment:
    __depth = None
    __qualityUtil = None
    __graphUtil = None
    __criteria = None
    __map = {
        0: 'gini',
        1: 'entropy'
    }

    def __init__(self):
        self.__qualityUtil = QualityUtil()
        self.__graphUtil = GraphUtil()

    def setParams(self, params):
        depth = params.get('depth')
        if depth is not None:
            self.__depth = int(depth)
        self.__criteria = params.get('criteria')

    def getResult(self, trainX, testX, trainY, testY):
        if self.__criteria is not None and self.__depth is not None:
            model = DecisionTreeClassifier(criterion=self.__criteria, max_depth=self.__depth)
            model.fit(trainX, trainY.values.ravel())
            predict = model.predict(testX)
            quality = self.__qualityUtil.getQuality(testY, predict)
            params = {
                'criteria': self.__criteria,
                'depth': self.__depth
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
        elif self.__criteria is not None:
            experiments = {}
            for i in range(1, len(trainX)):
                model = DecisionTreeClassifier(criterion=self.__criteria, max_depth=i)
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'criteria': self.__criteria,
                    'depth': i
                }
                result = {
                    'params': params,
                    'quality': quality,
                    'train': model.score(trainX, trainY)
                }
                experiments[i - 1] = result
            bestResult = self.__qualityUtil.getBestQualityExperiment(experiments)
            axis = self.__graphUtil.getAxis(experiments, 'depth')
            qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
            graphs = {
                0: self.__graphUtil.getLinePlot('Измение точности от depth - глубина дерева',
                                                axis.get('Точность').get('x'), axis.get('Точность').get('y'),
                                                'Глубина дерева', 'Точность'),
                1: self.__graphUtil.getLinePlot('Измение полноты от depth - глубина дерева',
                                                axis.get('Полнота').get('x'), axis.get('Полнота').get('y'),
                                                'Глубина дерева', 'Полнота'),
                2: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                               qualityGraphAxis.get('Точность').get('x'),
                                               qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
                3: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                               qualityGraphAxis.get('Полнота').get('x'),
                                               qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
            }
            bestResult['graphs'] = graphs
            return json.dumps(bestResult)
        elif self.__depth is not None:
            experiments = {}
            for i in range(0, len(self.__map)):
                model = DecisionTreeClassifier(criterion=self.__map.get(i), max_depth=self.__depth)
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'criteria': self.__map.get(i),
                    'depth': self.__depth
                }
                result = {
                    'params': params,
                    'quality': quality,
                    'train': model.score(trainX, trainY)
                }
                experiments[i] = result
            bestResult = self.__qualityUtil.getBestQualityExperiment(experiments)
            axis = self.__graphUtil.getAxis(experiments, 'criteria')
            qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
            graphs = {
                0: self.__graphUtil.getBarPlot('Изменение точности от критерия информативности',
                                               axis.get('Точность').get('x'), axis.get('Точность').get('y'),
                                               'Критерий информативности', 'Точность'),
                1: self.__graphUtil.getBarPlot('Изменение полноты от критерия информативности',
                                               axis.get('Полнота').get('x'), axis.get('Точность').get('y'),
                                               'Критерий информативности', 'Полнота'),
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
            for j in range(1, len(trainX)):
                model = DecisionTreeClassifier(criterion=self.__map[i], max_depth=j)
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'criteria': self.__map[i],
                    'depth': j
                }
                result = {
                    'params': params,
                    'quality': quality,
                    'train': model.score(trainX, trainY)
                }
                experiments[j - 1] = result
            bestExperiments[i] = self.__qualityUtil.getBestQualityExperiment(experiments)
            allExperiments[i] = experiments
        bestResult = self.__qualityUtil.getBestQualityExperiment(bestExperiments)
        bestCriteria = bestResult.get('params').get('criteria')
        invertMap = {v: k for k, v in self.__map.items()}
        axis = self.__graphUtil.getAxis(allExperiments.get(invertMap.get(bestCriteria)), 'depth')
        qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
        graphs = {
            0: self.__graphUtil.getLinePlot(
                'Измение точности от depth - глубина дерева, при критерии информативности ' + bestCriteria,
                axis.get('Точность').get('x'), axis.get('Точность').get('y'), 'Глубина дерева', 'Точность'),
            1: self.__graphUtil.getLinePlot(
                'Измение полноты от depth - глубина дерева, при критерии информативности ' + bestCriteria,
                axis.get('Полнота').get('x'), axis.get('Полнота').get('y'), 'Глубина дерева', 'Полнота'),
            2: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                           qualityGraphAxis.get('Точность').get('x'),
                                           qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
            3: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                           qualityGraphAxis.get('Полнота').get('x'),
                                           qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
        }
        bestResult['graphs'] = graphs
        return json.dumps(bestResult)
