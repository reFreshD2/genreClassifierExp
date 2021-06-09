from sklearn.neighbors import KNeighborsClassifier


class ClassifierFactory:

    def getClassifier(self, name, params):
        if name == 'KNeighbors':
            return KNeighborsClassifier(n_neighbors=params.get('k'))
