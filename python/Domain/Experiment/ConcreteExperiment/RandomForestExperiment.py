from sklearn.ensemble import RandomForestClassifier
from Util.QualityUtil import QualityUtil
from Util.GraphUtil import GraphUtil
import json


class RandomForestExperiment:
    N_ESTIMATORS_START = 50
    N_ESTIMATORS_END = 100
    DEPTH_START = 400
    DEPTH_END = 500
    __depth = None
    __qualityUtil = None
    __graphUtil = None
    __criteria = None
    __nEstimators = None
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
        nEstimators = params.get('nEstimators')
        if nEstimators is not None:
            self.__nEstimators = int(nEstimators)

    def getResult(self, trainX, testX, trainY, testY):
        maxFeatures = round(len(trainX.columns) ** 0.5)
        if self.__criteria is not None and self.__depth is not None and self.__nEstimators is not None:
            model = RandomForestClassifier(
                criterion=self.__criteria,
                max_depth=self.__depth,
                n_estimators=self.__nEstimators,
                max_features=maxFeatures
            )
            model.fit(trainX, trainY.values.ravel())
            predict = model.predict(testX)
            quality = self.__qualityUtil.getQuality(testY, predict)
            params = {
                'criteria': self.__criteria,
                'depth': self.__depth,
                'maxFeatures': maxFeatures,
                'nEstimators': self.__nEstimators
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
        elif self.__nEstimators is not None and self.__depth is not None:
            experiments = {}
            for i in range(0, len(self.__map)):
                model = RandomForestClassifier(
                    criterion=self.__map.get(i),
                    max_depth=self.__depth,
                    n_estimators=self.__nEstimators,
                    max_features=maxFeatures
                )
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'criteria': self.__map.get(i),
                    'depth': self.__depth,
                    'maxFeatures': maxFeatures,
                    'nEstimators': self.__nEstimators
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
        elif self.__criteria is not None and self.__depth is not None:
            experiments = {}
            for i in range(self.N_ESTIMATORS_START, self.N_ESTIMATORS_END):
                model = RandomForestClassifier(
                    criterion=self.__criteria,
                    max_depth=self.__depth,
                    n_estimators=i,
                    max_features=maxFeatures
                )
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'criteria': self.__criteria,
                    'depth': self.__depth,
                    'maxFeatures': maxFeatures,
                    'nEstimators': i
                }
                result = {
                    'params': params,
                    'quality': quality,
                    'train': model.score(trainX, trainY)
                }
                experiments[i - self.N_ESTIMATORS_START] = result
            bestResult = self.__qualityUtil.getBestQualityExperiment(experiments)
            axis = self.__graphUtil.getAxis(experiments, 'nEstimators')
            qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
            graphs = {
                0: self.__graphUtil.getLinePlot('Измение точности от nEstimators - количество деревьев',
                                                axis.get('Точность').get('x'),
                                                axis.get('Точность').get('y'), 'Количество деревьев', 'Точность'),
                1: self.__graphUtil.getLinePlot('Измение полноты от nEstimators', axis.get('Полнота').get('x'),
                                                axis.get('Полнота').get('y'), 'Количество деревьев', 'Полнота'),
                2: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                               qualityGraphAxis.get('Точность').get('x'),
                                               qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
                3: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                               qualityGraphAxis.get('Полнота').get('x'),
                                               qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
            }
            bestResult['graphs'] = graphs
            return json.dumps(bestResult)
        elif self.__criteria is not None and self.__nEstimators is not None:
            experiments = {}
            for i in range(1, len(trainX)):
                model = RandomForestClassifier(
                    criterion=self.__criteria,
                    max_depth=i,
                    n_estimators=self.__nEstimators,
                    max_features=maxFeatures
                )
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'criteria': self.__criteria,
                    'depth': i,
                    'maxFeatures': maxFeatures,
                    'nEstimators': self.__nEstimators
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
                                                axis.get('Точность').get('x'),
                                                axis.get('Точность').get('y'), 'Глубина дерева', 'Точность'),
                1: self.__graphUtil.getLinePlot('Измение полноты от depth - глубина дерева',
                                                axis.get('Полнота').get('x'),
                                                axis.get('Полнота').get('y'), 'Глубина дерева', 'Полнота'),
                2: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                               qualityGraphAxis.get('Точность').get('x'),
                                               qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
                3: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                               qualityGraphAxis.get('Полнота').get('x'),
                                               qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
            }
            bestResult['graphs'] = graphs
            return json.dumps(bestResult)
        elif self.__nEstimators is not None:
            allExperiments = {}
            bestExperiments = {}
            for i in range(0, len(self.__map)):
                experiments = {}
                for j in range(1, len(trainX)):
                    model = RandomForestClassifier(
                        criterion=self.__map.get(i),
                        max_depth=j,
                        n_estimators=self.__nEstimators,
                        max_features=maxFeatures
                    )
                    model.fit(trainX, trainY.values.ravel())
                    predict = model.predict(testX)
                    quality = self.__qualityUtil.getQuality(testY, predict)
                    params = {
                        'criteria': self.__map.get(i),
                        'depth': j,
                        'maxFeatures': maxFeatures,
                        'nEstimators': self.__nEstimators
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
                    axis.get('Точность').get('x'), axis.get('Точность').get('y'), 'Глубина дерева',
                    'Точность'),
                1: self.__graphUtil.getLinePlot(
                    'Измение полноты от depth - глубина дерева, при критерии информативности ' + bestCriteria,
                    axis.get('Полнота').get('x'), axis.get('Полнота').get('y'), 'Глубина дерева',
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
        elif self.__depth is not None:
            allExperiments = {}
            bestExperiments = {}
            for i in range(0, len(self.__map)):
                experiments = {}
                for j in range(self.N_ESTIMATORS_START, self.N_ESTIMATORS_END):
                    model = RandomForestClassifier(
                        criterion=self.__map.get(i),
                        max_depth=self.__depth,
                        n_estimators=j,
                        max_features=maxFeatures
                    )
                    model.fit(trainX, trainY.values.ravel())
                    predict = model.predict(testX)
                    quality = self.__qualityUtil.getQuality(testY, predict)
                    params = {
                        'criteria': self.__map.get(i),
                        'depth': self.__depth,
                        'maxFeatures': maxFeatures,
                        'nEstimators': j
                    }
                    result = {
                        'params': params,
                        'quality': quality,
                        'train': model.score(trainX, trainY)
                    }
                    experiments[j - self.N_ESTIMATORS_START] = result
                bestExperiments[i] = self.__qualityUtil.getBestQualityExperiment(experiments)
                allExperiments = experiments
            bestResult = self.__qualityUtil.getBestQualityExperiment(allExperiments)
            bestCriteria = bestResult.get('params').get('criteria')
            invertMap = {v: k for k, v in self.__map.items()}
            axis = self.__graphUtil.getAxis(allExperiments.get(invertMap.get(bestCriteria)), 'nEstimators')
            qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
            graphs = {
                0: self.__graphUtil.getLinePlot(
                    'Измение точности от nEstimators - количество деревьев, при критерии информативности '
                    + bestCriteria,
                    axis.get('Точность').get('x'), axis.get('Точность').get('y'), 'Количество деревьев', 'Точность'),
                1: self.__graphUtil.getLinePlot(
                    'Измение полноты от nEstimators - количество деревьев, при критерии информативности '
                    + bestCriteria,
                    axis.get('Полнота').get('x'), axis.get('Полнота').get('y'), 'Количество деревьев', 'Полнота'),
                2: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                               qualityGraphAxis.get('Точность').get('x'),
                                               qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
                3: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                               qualityGraphAxis.get('Полнота').get('x'),
                                               qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
            }
            bestResult['graphs'] = graphs
            return json.dumps(bestResult)
        elif self.__criteria is not None:
            allExperiments = {}
            bestExperiments = {}
            for i in range(self.DEPTH_START, self.DEPTH_END):
                experiments = {}
                for j in range(self.N_ESTIMATORS_START, self.N_ESTIMATORS_END):
                    model = RandomForestClassifier(
                        criterion=self.__criteria,
                        max_depth=i,
                        n_estimators=j,
                        max_features=maxFeatures
                    )
                    model.fit(trainX, trainY.values.ravel())
                    predict = model.predict(testX)
                    quality = self.__qualityUtil.getQuality(testY, predict)
                    params = {
                        'criteria': self.__criteria,
                        'depth': i,
                        'maxFeatures': maxFeatures,
                        'nEstimators': j
                    }
                    result = {
                        'params': params,
                        'quality': quality,
                        'train': model.score(trainX, trainY)
                    }
                    experiments[j - self.N_ESTIMATORS_START] = result
                bestExperiments[i - self.DEPTH_START] = self.__qualityUtil.getBestQualityExperiment(experiments)
                allExperiments[i - self.DEPTH_START] = experiments
            bestResult = self.__qualityUtil.getBestQualityExperiment(bestExperiments)
            bestDepth = bestResult.get('params').get('depth')
            axis = self.__graphUtil.getAxis(allExperiments.get(bestDepth - self.DEPTH_START), 'nEstimators')
            qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
            graphs = {
                0: self.__graphUtil.getLinePlot(
                    'Измение точности от nEstimators - количество деревьев, при глубине дереьев {}'.format(bestDepth),
                    axis.get('Точность').get('x'), axis.get('Точность').get('y'),
                    'Количество дереьев', 'Точность'),
                1: self.__graphUtil.getLinePlot(
                    'Измение полноты от nEstimators - количество деревьев, при глубине дереьев {}'.format(bestDepth),
                    axis.get('Полнота').get('x'), axis.get('Полнота').get('y'), 'Количество деревьев',
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
        allExperiments = {}
        experimentsForGraph = {}
        for i in range(0, len(self.__map)):
            bestExperiments = {}
            experimentsForGraphByEstimators = {}
            for j in range(self.DEPTH_START, self.DEPTH_END):
                experiments = {}
                for k in range(self.N_ESTIMATORS_START, self.N_ESTIMATORS_END):
                    model = RandomForestClassifier(
                        criterion=self.__map[i],
                        max_depth=j,
                        n_estimators=k,
                        max_features=maxFeatures
                    )
                    model.fit(trainX, trainY.values.ravel())
                    predict = model.predict(testX)
                    quality = self.__qualityUtil.getQuality(testY, predict)
                    params = {
                        'criteria': self.__map[i],
                        'depth': j,
                        'maxFeatures': maxFeatures,
                        'nEstimators': k
                    }
                    result = {
                        'params': params,
                        'quality': quality,
                        'train': model.score(trainX, trainY)
                    }
                    experiments[k - 2] = result
                bestExperiments[j - 1] = self.__qualityUtil.getBestQualityExperiment(experiments)
                experimentsForGraphByEstimators[j - 1] = experiments
            allExperiments[i] = self.__qualityUtil.getBestQualityExperiment(bestExperiments)
            bestExperimentIndex = allExperiments.get(i).get('params').get('depth')
            experimentsForGraph[i] = experimentsForGraphByEstimators.get(bestExperimentIndex)
        bestResult = self.__qualityUtil.getBestQualityExperiment(allExperiments)
        invertMap = {v: k for k, v in self.__map.items()}
        bestCriteria = bestResult.get('params').get('criteria')
        axis = self.__graphUtil.getAxis(allExperiments.get(invertMap.get(bestCriteria)), 'nEstimators')
        qualityGraphAxis = self.__graphUtil.getQualityByGenre(bestResult.get('quality'))
        graphs = {
            0: self.__graphUtil.getLinePlot(
                'Измение точности от nEstimators - количество деревьев, при критерии информативности '
                + bestCriteria
                + ' и глубине дерева' + bestResult.get('params').get('depth'),
                axis.get('Точность').get('x'), axis.get('Точность').get('y'), 'Количество деревьев', 'Точность'),
            1: self.__graphUtil.getLinePlot(
                'Измение точности от nEstimators - количество деревьев, при критерии информативности '
                + bestCriteria
                + ' и глубине дерева' + bestResult.get('params').get('depth'),
                axis.get('Полнота').get('x'), axis.get('Полнота').get('y'), 'Количество деревьев', 'Полнота'),
            2: self.__graphUtil.getBarPlot('Точность классификации для каждого жанра',
                                           qualityGraphAxis.get('Точность').get('x'),
                                           qualityGraphAxis.get('Точность').get('y'), 'Жанры', 'Точность'),
            3: self.__graphUtil.getBarPlot('Полнота классификации для каждого жанра',
                                           qualityGraphAxis.get('Полнота').get('x'),
                                           qualityGraphAxis.get('Полнота').get('y'), 'Жанры', 'Полнота')
        }
        bestResult['graphs'] = graphs
        return json.dumps(bestResult)
