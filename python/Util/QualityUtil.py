from sklearn.metrics import confusion_matrix
from Util.DataSetUtil import DataSetUtil


class QualityUtil:
    __dataSetUtil = None

    def __init__(self):
        self.__dataSetUtil = DataSetUtil()

    def getQuality(self, trueY, predictY):
        result = {}
        matrix = confusion_matrix(trueY, predictY)
        sumPrecision = 0
        sumRecall = 0
        for i in range(0, matrix.shape[0]):
            elem = matrix[i][i]
            sumColumn = 0
            sumRaw = 0
            for j in range(0, matrix.shape[0]):
                sumColumn += matrix[j][i]
                sumRaw += matrix[i][j]
            precision = elem / sumRaw
            if sumColumn != 0:
                recall = elem / sumColumn
            else:
                recall = 0
            sumPrecision += precision
            sumRecall += recall
            quality = {
                'Точность': precision,
                'Полнота': recall
            }
            result[self.__dataSetUtil.getTargetName(i)] = quality
        result['Средняя точность'] = sumPrecision / matrix.shape[0]
        result['Средняя полнота'] = sumRecall / matrix.shape[0]
        return result

    def getBestQualityExperiment(self, experiments):
        bestIndex = 0
        bestPrecision = experiments.get(0).get('quality').get('Средняя точность')
        bestRecall = experiments.get(0).get('quality').get('Средняя полнота')
        for i in range(1, len(experiments)):
            currentPrecision = experiments.get(i).get('quality').get('Средняя точность')
            currentRecall = experiments.get(i).get('quality').get('Средняя полнота')
            if bestPrecision < currentPrecision and bestRecall < currentRecall:
                bestIndex = i
                bestPrecision = currentPrecision
                bestRecall = currentRecall
        return experiments.get(bestIndex)
