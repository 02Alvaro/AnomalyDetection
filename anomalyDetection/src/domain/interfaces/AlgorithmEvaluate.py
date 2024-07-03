from abc import abstractmethod

from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


class AlgorithmEvaluate:
    """
    Abstract base class for algorithm evaluation.

    Methods
    -------
    evaluate(algorithm_data: AlgorithmConfigurator)
        Abstract method for evaluating the algorithm with the given configuration.
    """

    @abstractmethod
    def evaluate(self, algorithm_data: AlgorithmConfigurator):
        """
        Evaluates the algorithm with the given configuration.

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
