from abc import abstractmethod

from domain.interfaces.AlgorithmData import AlgorithmData


class TrainRepository:
    @abstractmethod
    def save(algorithmData: AlgorithmData):
        pass
