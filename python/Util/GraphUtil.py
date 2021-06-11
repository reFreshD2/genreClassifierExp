import base64
import io

from matplotlib import pyplot as plt


class GraphUtil:

    def getGraph(self, title, axisX, axisY, labelX, labelY):
        image = io.BytesIO()
        plt.plot(axisX, axisY, linewidth=2)
        plt.xlabel(labelX)
        plt.ylabel(labelY)
        plt.title(title)
        plt.savefig(image, format='jpg')
        plt.close()
        image.seek(0)
        return base64.b64encode(image.read()).decode('utf-8')
