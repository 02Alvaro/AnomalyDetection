from abc import abstractmethod

from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


class AlgorithmTrainer:
    """
    Abstract base class for algorithm training.

    Methods
    -------
    train(algorithm_data: AlgorithmConfigurator)
        Abstract method for training the algorithm with the given configuration.
    """

    @abstractmethod
    def train(self, algorithm_data: AlgorithmConfigurator):
        """
        Trains the algorithm with the given configuration.

        Parameters
        ----------
        algorithm_data : AlgorithmConfigurator
            The configuration data for the algorithm.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in the derived class.
        """
        pass
