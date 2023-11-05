from abc import abstractmethod

from domain.interfaces.AlgorithmData import AlgorithmData


class AlgorithmExecutor:
    @abstractmethod
    def execute(self, algorithm_data: AlgorithmData):
        pass
