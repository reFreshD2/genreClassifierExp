from Domain.Experiment.ConcreteExperiment.KNeighborsExperiment import KNeighborsExperiment
from Domain.Experiment.ConcreteExperiment.KNeighborsWeightExperiment import KNeighborsWeightExperiment
from Domain.Experiment.ConcreteExperiment.ParzenExperiment import ParzenExperiment
from Domain.Experiment.ConcreteExperiment.DecisionTreeExperiment import DecisionTreeExperiment
from Domain.Experiment.ConcreteExperiment.RandomForestExperiment import RandomForestExperiment
from Domain.Experiment.ConcreteExperiment.SVCExperiment import SVCExperiment
from Domain.Experiment.ConcreteExperiment.SGDExperiment import SGDExperiment


class ExperimentFactory:
    __map = {
        'KNeighbors': KNeighborsExperiment(),
        'KNeighborsWeight': KNeighborsWeightExperiment(),
        'Parzen': ParzenExperiment(),
        'DecisionTree': DecisionTreeExperiment(),
        'RandomForest': RandomForestExperiment(),
        'SVC': SVCExperiment(),
        'SGD': SGDExperiment()
    }

    def getExperiment(self, name, params):
        experiment = self.__map.get(name)
        experiment.setParams(params)
        return experiment
