from dataclasses import dataclass


@dataclass
class AlgorithmConfigurator:
    data_file: str = "multi-dataset.csv"
    model_name: str = "model.pkl"
    report_file: str = "report.csv"
    seed: int = 42
