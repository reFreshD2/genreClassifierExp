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
        avgPrecision = sumPrecision / matrix.shape[0]
        avgRecall = sumRecall / matrix.shape[0]
        result['Средняя точность'] = avgPrecision
        result['Средняя полнота'] = avgRecall
        result['F-мера'] = 2 * avgRecall * avgPrecision / (avgRecall + avgPrecision)
        return result

    def getBestQualityExperiment(self, experiments):
        bestIndex = 0
        bestQuality = experiments.get(0).get('quality').get('F-мера')
        for i in range(1, len(experiments)):
            currentQuality = experiments.get(i).get('quality').get('F-мера')
            if bestQuality < currentQuality:
                bestIndex = i
                bestQuality = currentQuality
        return experiments.get(bestIndex)
