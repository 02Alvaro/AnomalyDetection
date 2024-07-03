import json
import os
from dataclasses import asdict

from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator
from domain.interfaces.TrainRepository import TrainRepository


class TrainRepositoryInFile(TrainRepository):
    """
    Class for saving algorithm training data to a file.

    Attributes
    ----------
    file_path : str
        The path to the directory where the training data file will be saved.
    """

    def __init__(self, file_path: str):
        """
        Initializes the TrainRepositoryInFile with the given file path.

        Parameters
        ----------
        file_path : str
            The path to the directory where the training data file will be saved.
        """
        self.file_path = file_path

    def save(self, algorithmData: AlgorithmConfigurator, filename="all_models.csv"):
        """
        Saves the given algorithm configuration data to a CSV file.

        Parameters
        ----------
        algorithmData : AlgorithmConfigurator
            The algorithm configuration data to be saved.
        filename : str, optional
            The name of the file to save the data, by default "all_models.csv".
        """
        header = "Algorithm,data_file,model_name,params\n"
        file_path = os.path.join(self.file_path, filename)

        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(header)

        data_dict = asdict(algorithmData)
        name = algorithmData.__class__.__name__.replace("Configuration", "")

        data_file = data_dict.pop("data_file")
        model_name = data_dict.pop("model_name")
        data_dict.pop("report_file")

        # Convert each dictionary value to an appropriate string
        processed_params = {
            k: json.dumps(v) if isinstance(v, (list, tuple)) else v
            for k, v in data_dict.items()
        }

        # Convert the processed parameters dictionary to a string for the parameters column
        parameters_str = ";".join(f"{k}: {v}" for k, v in processed_params.items())

        # Use a different variable name to avoid conflict
        csv_line = f"{name},{data_file},{model_name},{parameters_str}\n"

        with open(file_path, "a") as f:
            f.write(csv_line)
            print(csv_line)
