from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


class ExecuterNotFound(Exception):
    """
    Exception raised when an executor for a specified algorithm is not found.

    Parameters
    ----------
    algorithm : AlgorithmConfigurator
        The algorithm configuration whose executor was not found.

    Attributes
    ----------
    message : str
        The error message indicating that the executor for the specified algorithm was not found.
    """

    def __init__(self, algorithm: AlgorithmConfigurator):
        """
        Initializes the ExecuterNotFound exception with the given algorithm configuration.

        Parameters
        ----------
        algorithm : AlgorithmConfigurator
            The algorithm configuration whose executor was not found.
        """
        message = f"Executer for '{algorithm.__class__.__name__}' not found"
        super().__init__(message)
