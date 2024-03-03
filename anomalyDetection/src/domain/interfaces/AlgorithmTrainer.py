from abc import abstractmethod

from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


class AlgorithmTrainer:
    @abstractmethod
    def train(self, algorithm_data: AlgorithmConfigurator):
        pass
