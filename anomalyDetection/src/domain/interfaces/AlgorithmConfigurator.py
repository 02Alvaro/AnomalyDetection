from dataclasses import dataclass


@dataclass
class AlgorithmConfigurator:
    """
    Configuration class for algorithm settings.

    Attributes
    ----------
    data_file : str
        The name of the data file to be used (default is "multi-dataset.csv").
    model_name : str
        The name of the model file to be used (default is "model.pkl").
    report_file : str
        The name of the report file to be generated (default is "report.csv").
    seed : int
        The seed value for random number generation (default is 42).
    """
    data_file: str = "multi-dataset.csv"
    model_name: str = "model.pkl"
    report_file: str = "report.csv"
    seed: int = 42
