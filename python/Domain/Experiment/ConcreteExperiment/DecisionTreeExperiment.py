from sklearn.tree import DecisionTreeClassifier
from Util.QualityUtil import QualityUtil
from Util.GraphUtil import GraphUtil
import json


class DecisionTreeExperiment:
    __depth = None
    __qualityUtil = None
    __graphUtil = None
    __criteria = None
    __map = ['gini', 'entropy']

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
                'quality': quality
            }
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
            graphs = {
                '0': self.__graphUtil.getGraph(
                    'Измение точности от depth',
                    axis.get('Точность').get('x'),
                    axis.get('Точность').get('y'),
                    'depth',
                    'Точность'
                ),
                '1': self.__graphUtil.getGraph(
                    'Измение полноты от depth',
                    axis.get('Полнота').get('x'),
                    axis.get('Полнота').get('y'),
                    'depth',
                    'Полнота'
                )
            }
            bestResult['graphs'] = graphs
            return json.dumps(bestResult)
        elif self.__depth is not None:
            experiments = {}
            for i in range(0, len(self.__map)):
                model = DecisionTreeClassifier(criterion=self.__map[i], max_depth=self.__depth)
                model.fit(trainX, trainY.values.ravel())
                predict = model.predict(testX)
                quality = self.__qualityUtil.getQuality(testY, predict)
                params = {
                    'criteria': self.__map[i],
                    'depth': self.__depth
                }
                result = {
                    'params': params,
                    'quality': quality,
                    'train': model.score(trainX, trainY)
                }
                experiments[i] = result
            bestResult = self.__qualityUtil.getBestQualityExperiment(experiments)
            return json.dumps(bestResult)
        allExperiments = {}
        graphs = {}
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
            allExperiments[i] = self.__qualityUtil.getBestQualityExperiment(experiments)
            axis = self.__graphUtil.getAxis(experiments, 'depth')
            graphs[i * 2] = self.__graphUtil.getGraph(
                'Измение точности от depth при критерии информативности ' + self.__map[i],
                axis.get('Точность').get('x'),
                axis.get('Точность').get('y'),
                'depth',
                'Точность'
            )
            graphs[i * 2 + 1] = self.__graphUtil.getGraph(
                'Измение полноты от depth при критерии информативности ' + self.__map[i],
                axis.get('Полнота').get('x'),
                axis.get('Полнота').get('y'),
                'depth',
                'Полнота'
            )
        bestResult = self.__qualityUtil.getBestQualityExperiment(allExperiments)
        bestResult['graphs'] = graphs
        return json.dumps(bestResult)
