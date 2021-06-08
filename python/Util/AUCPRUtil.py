import base64

from matplotlib import pyplot as plt
from sklearn import metrics
import io


class AUCPRUtil:
    __yTrue = None
    __yScore = None

    def __init__(self, yTrue, yScore):
        self.__yTrue = yTrue
        self.__yScore = yScore

    def gerAUC(self):
        precision, recall, thresholds = metrics.precision_recall_curve(self.__yTrue, self.__yScore)
        return metrics.auc(precision, recall)

    def getGraph(self):
        precision, recall, thresholds = metrics.precision_recall_curve(self.__yTrue, self.__yScore)
        image = io.BytesIO()
        plt.plot(recall, precision, linewidth=2)
        plt.xlabel('Полнота')
        plt.ylabel('Точность')
        plt.title('Кривая точность-полнота')
        plt.savefig(image, format='jpg')
        image.seek(0)
        return base64.b64encode(image.read())
