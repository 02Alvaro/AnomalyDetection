import os

from domain.interfaces.ReportInterface import ReportInterface
from domain.models.BasicReport import BasicReport


class ReportInFile(ReportInterface):
    """
    Class for saving report metrics to a file.

    Attributes
    ----------
    file_path : str
        The path to the directory where the report file will be saved.
    """

    def __init__(self, file_path: str):
        """
        Initializes the ReportInFile with the given file path.

        Parameters
        ----------
        file_path : str
            The path to the directory where the report file will be saved.
        """
        self.file_path = file_path

    def save(self, metrics: BasicReport, filename: str = "all_results.csv"):
        """
        Saves the given metrics to a CSV file.

        Parameters
        ----------
        metrics : BasicReport
            The evaluation metrics to be saved.
        filename : str, optional
            The name of the file to save the metrics, by default "all_results.csv".
        """
        header = "Algorithm,model,dataset,samples,dims,anomaly_rate,time,se,sp,p,roc\n"
        file_path = os.path.join(self.file_path, filename)

        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(header)

        with open(file_path, "a") as f:
            f.write(str(metrics) + "\n")
        print(metrics)
