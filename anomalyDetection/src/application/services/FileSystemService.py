import os

import pandas as pd
from domain.enums.PathKey import PathKey


class FileSystemService:
    """
    Service class for handling file system operations.

    Attributes
    ----------
    base_path : str
        The base path for all file operations.
    paths : dict
        A dictionary mapping PathKey enums to subdirectories.
    """

    def __init__(self, base_path, paths):
        """
        Initializes the FileSystemService with the given base path and paths.

        Parameters
        ----------
        base_path : str
            The base path for all file operations.
        paths : dict
            A dictionary mapping PathKey enums to subdirectories.
        """
        self.base_path = base_path
        self.paths = paths

    def get_path(self, key: PathKey, filename: str):
        """
        Constructs the full path for the given key and filename.

        Parameters
        ----------
        key : PathKey
            The key representing the type of path.
        filename : str
            The name of the file.

        Returns
        -------
        str
            The full path to the file.

        Raises
        ------
        ValueError
            If the specified key is invalid.
        """
        if key in self.paths:
            return os.path.join(self.base_path, self.paths[key], filename)
        else:
            raise ValueError(f"Invalid key specified: {key}")

    def read_resultsFrom(self, filename):
        """
        Reads results from a CSV file.

        Parameters
        ----------
        filename : str
            The name of the file containing the results.

        Returns
        -------
        pd.DataFrame
            The DataFrame containing the results.
        """
        file_path = self.get_path(PathKey.RESULTS, filename)
        return pd.read_csv(file_path)

    def read_dataFrom(self, filename):
        """
        Reads data from a CSV file.

        Parameters
        ----------
        filename : str
            The name of the file containing the data.

        Returns
        -------
        pd.DataFrame
            The DataFrame containing the data.
        """
        file_path = self.get_path(PathKey.DATA, filename)
        return pd.read_csv(file_path)

    def save_metricsTo(self, filename, metrics):
        """
        Saves metrics to a CSV file.

        Parameters
        ----------
        filename : str
            The name of the file to save the metrics.
        metrics : pd.DataFrame
            The DataFrame containing the metrics.
        """
        file_path = self.get_path(PathKey.METRICS, filename)
        metrics.to_csv(file_path, index=False)

    def save_resultsTo(self, filename, results):
        """
        Saves results to a CSV file.

        Parameters
        ----------
        filename : str
            The name of the file to save the results.
        results : pd.DataFrame
            The DataFrame containing the results.
        """
        file_path = self.get_path(PathKey.RESULTS, filename)
        results.to_csv(file_path, index=False)

    def get_results_path(self):
        """
        Gets the path to the results directory.

        Returns
        -------
        str
            The path to the results directory.
        """
        return self.get_path(PathKey.RESULTS, "")
