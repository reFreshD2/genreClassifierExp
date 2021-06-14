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

    def getLinePlot(self, title, axisX, axisY, labelX, labelY):
        image = io.BytesIO()
        plt.plot(axisX, axisY, linewidth=2)
        plt.xlabel(labelX)
        plt.ylabel(labelY)
        plt.title(title)
        plt.savefig(image, format='jpg')
        plt.close()
        image.seek(0)
        return base64.b64encode(image.read()).decode('utf-8')

    def getBarPlot(self, title, names, axisY, labelX, labelY):
        image = io.BytesIO()
        plt.bar(names, axisY)
        plt.xlabel(labelX)
        plt.ylabel(labelY)
        plt.title(title)
        plt.savefig(image, format='jpg')
        plt.close()
        image.seek(0)
        return base64.b64encode(image.read()).decode('utf-8')
