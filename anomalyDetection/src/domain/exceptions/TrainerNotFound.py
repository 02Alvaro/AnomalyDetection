from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


class TrainerNotFound(Exception):
    """
    Exception raised when a trainer for a specified algorithm is not found.

    Parameters
    ----------
    algorithm : AlgorithmConfigurator
        The algorithm configuration whose trainer was not found.

    Attributes
    ----------
    message : str
        The error message indicating that the trainer for the specified algorithm was not found.
    """

    def __init__(self, algorithm: AlgorithmConfigurator):
        """
        Initializes the TrainerNotFound exception with the given algorithm configuration.

        Parameters
        ----------
        algorithm : AlgorithmConfigurator
            The algorithm configuration whose trainer was not found.
        """
        message = f"Trainer for '{algorithm.__class__.__name__}' not found"
        super().__init__(message)
