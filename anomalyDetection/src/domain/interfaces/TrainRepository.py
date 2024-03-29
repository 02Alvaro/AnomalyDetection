from abc import abstractmethod

from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


class TrainRepository:
    @abstractmethod
    def save(algorithmData: AlgorithmConfigurator):
        pass
