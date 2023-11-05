from abc import abstractmethod

from domain.interfaces.AlgorithmExecutor import AlgorithmExecutor


class SupervisedAlgorithmExecutor(AlgorithmExecutor):
    @abstractmethod
    def execute(self, algorithm_data):
        pass
