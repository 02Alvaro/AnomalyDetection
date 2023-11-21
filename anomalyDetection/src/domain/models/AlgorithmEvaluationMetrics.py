from dataclasses import dataclass


@dataclass
class AlgorithmEvaluationMetrics:
    algorithm_name: str
    algorithm_parameters: dict
    dataset_name: str
    num_examples: int
    num_dims: int
    anomaly_percentage: float
    metrics: dict

    def __init__(
        self,
        algorithmData,
        dataset_name,
        num_examples,
        num_dims,
        anomaly_percentage,
        metrics,
    ):
        self.algorithmData = algorithmData
        self.dataset_name = dataset_name
        self.num_examples = num_examples
        self.num_dims = num_dims
        self.anomaly_percentage = anomaly_percentage
        self.metrics = metrics
