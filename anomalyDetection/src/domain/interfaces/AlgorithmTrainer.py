from abc import abstractmethod

from domain.interfaces.AlgorithmData import AlgorithmData


class AlgorithmTrainer:
    @abstractmethod
    def train(self, algorithm_data: AlgorithmData):
        pass
