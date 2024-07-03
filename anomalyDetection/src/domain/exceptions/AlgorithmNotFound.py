class AlgorithmDataNotFound(Exception):
    """
    Exception raised when algorithm data is not found.

    Parameters
    ----------
    name : str
        The name of the algorithm whose data was not found.

    Attributes
    ----------
    message : str
        The error message indicating that the algorithm data was not found.
    """

    def __init__(self, name: str):
        """
        Initializes the AlgorithmDataNotFound exception with the given algorithm name.

        Parameters
        ----------
        name : str
            The name of the algorithm whose data was not found.
        """
        message = f"AlgorithmData for '{name}' not found"
        super().__init__(message)
