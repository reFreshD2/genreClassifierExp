from sklearn.ensemble import RandomForestClassifier
from Util.QualityUtil import QualityUtil
from Util.GraphUtil import GraphUtil
import json


class RandomForestExperiment:
    N_ESTIMATORS_START = 2
    N_ESTIMATORS_END = 100
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
            graphs = {
                0: self.__graphUtil.getBarPlot('Изменение точности от критерия информативности',
                                               axis.get('Точность').get('x'), axis.get('Точность').get('y'),
                                               'Критерий информативности', 'Точность'),
                1: self.__graphUtil.getBarPlot('Изменение полноты от критерия информативности',
                                               axis.get('Полнота').get('x'), axis.get('Точность').get('y'),
                                               'Критерий информативности', 'Полнота'),
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
                experiments[i - 2] = result
            bestResult = self.__qualityUtil.getBestQualityExperiment(experiments)
            axis = self.__graphUtil.getAxis(experiments, 'nEstimators')
            graphs = {
                self.__graphUtil.getLinePlot('Измение точности от nEstimators', axis.get('Точность').get('x'),
                                             axis.get('Точность').get('y'), 'nEstimators', 'Точность'),
                self.__graphUtil.getLinePlot('Измение полноты от nEstimators', axis.get('Полнота').get('x'),
                                             axis.get('Полнота').get('y'), 'nEstimators', 'Полнота')
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
            graphs = {
                self.__graphUtil.getLinePlot('Измение точности от depth', axis.get('Точность').get('x'),
                                             axis.get('Точность').get('y'), 'depth', 'Точность'),
                self.__graphUtil.getLinePlot('Измение полноты от depth', axis.get('Полнота').get('x'),
                                             axis.get('Полнота').get('y'), 'depth', 'Полнота')
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
            graphs = {
                self.__graphUtil.getLinePlot('Измение точности от depth при критерии информативности ' + bestCriteria,
                                             axis.get('Точность').get('x'), axis.get('Точность').get('y'), 'depth',
                                             'Точность'),
                self.__graphUtil.getLinePlot('Измение полноты от depth при критерии информативности ' + bestCriteria,
                                             axis.get('Полнота').get('x'), axis.get('Полнота').get('y'), 'depth',
                                             'Полнота')
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
                    experiments[j - 2] = result
                bestExperiments[i] = self.__qualityUtil.getBestQualityExperiment(experiments)
                allExperiments = experiments
            bestResult = self.__qualityUtil.getBestQualityExperiment(allExperiments)
            bestCriteria = bestResult.get('params').get('criteria')
            invertMap = {v: k for k, v in self.__map.items()}
            axis = self.__graphUtil.getAxis(allExperiments.get(invertMap.get(bestCriteria)), 'nEstimators')
            graphs = {
                self.__graphUtil.getLinePlot(
                    'Измение точности от nEstimators при критерии информативности ' + bestCriteria,
                    axis.get('Точность').get('x'), axis.get('Точность').get('y'), 'nEstimators', 'Точность'),
                self.__graphUtil.getLinePlot(
                    'Измение полноты от nEstimators при критерии информативности ' + bestCriteria,
                    axis.get('Полнота').get('x'), axis.get('Полнота').get('y'), 'nEstimators', 'Полнота')
            }
            bestResult['graphs'] = graphs
            return json.dumps(bestResult)
        elif self.__criteria is not None:
            allExperiments = {}
            bestExperiments = {}
            for i in range(1, len(trainX)):
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
                    experiments[j - 2] = result
                bestExperiments[i - 1] = self.__qualityUtil.getBestQualityExperiment(experiments)
                allExperiments[i - 1] = experiments
            bestResult = self.__qualityUtil.getBestQualityExperiment(bestExperiments)
            bestDepth = bestResult.get('params').get('depth')
            axis = self.__graphUtil.getAxis(allExperiments.get(bestDepth - 1), 'nEstimators')
            graphs = {
                self.__graphUtil.getLinePlot('Измение точности от nEstimators при depth ' + bestDepth,
                                             axis.get('Точность').get('x'), axis.get('Точность').get('y'),
                                             'nEstimators', 'Точность'),
                self.__graphUtil.getLinePlot('Измение полноты от nEstimators при depth ' + bestDepth,
                                             axis.get('Полнота').get('x'), axis.get('Полнота').get('y'), 'nEstimators',
                                             'Полнота')
            }
            bestResult['graphs'] = graphs
            return json.dumps(bestResult)
        allExperiments = {}
        graphs = {}
        for i in range(0, len(self.__map)):
            bestExperiments = {}
            for j in range(1, 500):
                experiments = {}
                for k in range(2, 100):
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
                axis = self.__graphUtil.getAxis(experiments, 'nEstimators')
                graphs[(j - 1) * 2] = self.__graphUtil.getLinePlot(
                    'Измение точности от nEstimators при depth %d и критерии %s'.format(j, self.__map[i]),
                    axis.get('Точность').get('x'), axis.get('Точность').get('y'), 'nEstimators', 'Точность')
                graphs[(j - 1) * 2 + 1] = self.__graphUtil.getLinePlot(
                    'Измение полноты от nEstimators при depth %d и критерии %s'.format(i, self.__map[i]),
                    axis.get('Полнота').get('x'), axis.get('Полнота').get('y'), 'nEstimators', 'Полнота')
            allExperiments[i] = self.__qualityUtil.getBestQualityExperiment(bestExperiments)
        bestResult = self.__qualityUtil.getBestQualityExperiment(allExperiments)
        bestResult['graphs'] = graphs
        return json.dumps(bestResult)
