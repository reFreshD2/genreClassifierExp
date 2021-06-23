import base64
import io

from matplotlib import pyplot as plt


class GraphUtil:

    def getAxis(self, experiments, xName):
        x = []
        yPrecision = []
        yRecall = []
        for i in range(0, len(experiments)):
            x.append(experiments.get(i).get('params').get(xName))
            yPrecision.append(experiments.get(i).get('quality').get('Средняя точность'))
            yRecall.append(experiments.get(i).get('quality').get('Средняя полнота'))
        return {
            'Точность': {
                'x': x,
                'y': yPrecision
            },
            'Полнота': {
                'x': x,
                'y': yRecall
            }
        }

    def getQualityByGenre(self, quality):
        x = []
        yPrecision = []
        yRecall = []
        for qualityKey, qualityValue in quality.items():
            if qualityKey != 'Средняя точность' and qualityKey != 'Средняя полнота' and qualityKey != 'F-мера':
                x.append(qualityKey)
                yPrecision.append(qualityValue.get('Точность'))
                yRecall.append(qualityValue.get('Полнота'))
        return {
            'Точность': {
                'x': x,
                'y': yPrecision
            },
            'Полнота': {
                'x': x,
                'y': yRecall
            }
        }

    def getLinePlot(self, title, axisX, axisY, labelX, labelY):
        image = io.BytesIO()
        plt.plot(axisX, axisY, linewidth=2)
        plt.xlabel(labelX)
        plt.ylabel(labelY)
        plt.title(title, fontsize=8)
        plt.savefig(image, format='jpg')
        plt.close()
        image.seek(0)
        return base64.b64encode(image.read()).decode('utf-8')

    def getBarPlot(self, title, names, axisY, labelX, labelY):
        image = io.BytesIO()
        if labelX != 'Жанры':
            plt.bar(names, axisY)
        else:
            plt.barh(names, axisY)
        plt.xlabel(labelX)
        plt.ylabel(labelY)
        plt.title(title, fontsize=8)
        plt.savefig(image, format='jpg')
        plt.close()
        image.seek(0)
        return base64.b64encode(image.read()).decode('utf-8')
