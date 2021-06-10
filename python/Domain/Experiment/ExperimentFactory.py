from Domain.Experiment.ConcreteExperiment.KNeighborsExperiment import KNeighborsExperiment


class ExperimentFactory:
    __map = {
        'KNeighbors': KNeighborsExperiment()
    }

    def getExperiment(self, name, params):
        experiment = self.__map.get(name)
        experiment.setParams(params)
        return experiment
