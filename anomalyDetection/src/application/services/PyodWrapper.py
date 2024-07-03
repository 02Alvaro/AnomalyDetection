import os
from dataclasses import dataclass, field

from application.services.FileSystemService import FileSystemService
from joblib import dump, load


@dataclass
class PyodParameters:
    """
    Data class for storing parameters related to PyOD algorithms.

    Attributes
    ----------
    algorithm_name : str
        The name of the algorithm.
    contamination : float
        The contamination rate of the data set.
    params : dict
        Additional parameters for the algorithm.
    """
    algorithm_name: str
    contamination: float
    params: dict = field(default_factory=dict)


class PyodWrapper:
    """
    Wrapper class for saving and loading PyOD models.

    Attributes
    ----------
    file_system_service : FileSystemService
        Service for file system operations.
    """

    def __init__(
        self,
        file_system_service: FileSystemService,
    ):
        """
        Initializes the PyodWrapper with the provided file system service.

        Parameters
        ----------
        file_system_service : FileSystemService
            Service for file system operations.
        """
        self.file_system_service = file_system_service

    def saveModel(self, model, filename):
        """
        Saves the PyOD model to a file.

        Parameters
        ----------
        model : object
            The PyOD model to be saved.
        filename : str
            The name of the file to save the model.
        """
        dump(
            model,
            os.path.join(self.file_system_service.get_results_path(), filename),
            protocol=4,
        )

    def loadModel(self, filename):
        """
        Loads a PyOD model from a file.

        Parameters
        ----------
        filename : str
            The name of the file containing the model.

        Returns
        -------
        object
            The loaded PyOD model.
        """
        return load(
            os.path.join(self.file_system_service.get_results_path(), filename))
