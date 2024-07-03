from abc import abstractmethod

from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


class TrainRepository:
    """
    Abstract base class for training data repository.

    Methods
    -------
    save(algorithmData: AlgorithmConfigurator)
        Abstract method for saving the training data.
    """

    @abstractmethod
    def save(self, algorithmData: AlgorithmConfigurator):
        """
        Saves the training data.

        Parameters
        ----------
        algorithmData : AlgorithmConfigurator
            The configuration data for the algorithm to be saved.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in the derived class.
        """
        pass
