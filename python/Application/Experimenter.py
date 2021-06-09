import json
from Domain.Classifier.ClassifierFactory import ClassifierFactory
from Util.DataSetUtil import DataSetUtil


class Experimenter:
    __factory = None
    __dataSetUtil = None

    def __init__(self):
        self.__factory = ClassifierFactory()
        self.__dataSetUtil = DataSetUtil()

    def handle(self, params):
        paramsDecoding = json.loads(params)
        dataSet = self.__dataSetUtil.getDataSet(params.get('count'), params.get('type'))
        return dataSet
