from sklearn.metrics import confusion_matrix


class QualityUtil:

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
            recall = elem / sumColumn
            sumPrecision += precision
            sumRecall += recall
            quality = {
                'Точность': precision,
                'Полнопа': recall
            }
            result[i] = quality
        result['Средняя точность'] = sumPrecision / matrix.shape[0]
        result['Средняя полнота'] = sumRecall / matrix.shape[0]
        return result
