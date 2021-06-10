import json
from Domain.Experiment.ExperimentFactory import ExperimentFactory
from Util.DataSetUtil import DataSetUtil


class Experimenter:
    __factory = None
    __dataSetUtil = None

    def __init__(self):
        self.__factory = ExperimentFactory()
        self.__dataSetUtil = DataSetUtil()

    def handle(self, params):
        paramsDecoding = json.loads(params)
        trainX, testX, trainY, testY = self.__dataSetUtil.getTrainTestSplit(
            paramsDecoding.get('count'),
            paramsDecoding.get('type')
        )
        experimenter = self.__factory.getExperiment(paramsDecoding.get('method'), paramsDecoding)
        return experimenter.getResult(trainX, testX, trainY, testY)
