from Domain.Experiment.ConcreteExperiment.KNeighborsExperiment import KNeighborsExperiment
from Domain.Experiment.ConcreteExperiment.KNeighborsWeightExperiment import KNeighborsWeightExperiment
from Domain.Experiment.ConcreteExperiment.ParzenExperiment import ParzenExperiment
from Domain.Experiment.ConcreteExperiment.DecisionTreeExperiment import DecisionTreeExperiment
from Domain.Experiment.ConcreteExperiment.RandomForestExperiment import RandomForestExperiment


class ExperimentFactory:
    __map = {
        'KNeighbors': KNeighborsExperiment(),
        'KNeighborsWeight': KNeighborsWeightExperiment(),
        'Parzen': ParzenExperiment(),
        'DecisionTree': DecisionTreeExperiment(),
        'RandomForest': RandomForestExperiment()
    }

    def getExperiment(self, name, params):
        experiment = self.__map.get(name)
        experiment.setParams(params)
        return experiment
