from dataclasses import dataclass


@dataclass
class AlgorithmConfigurator:
    data_file: str
    model_name: str
    report_file: str
    seed: int = 42
