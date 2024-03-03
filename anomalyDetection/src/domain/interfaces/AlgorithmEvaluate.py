from abc import abstractmethod

from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


class AlgorithmEvaluate:
    @abstractmethod
    def evaluate(self, algorithm_data: AlgorithmConfigurator):
        pass
