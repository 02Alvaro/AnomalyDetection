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
        algorithm_name,
        algorithm_parameters,
        dataset_name,
        num_examples,
        num_dims,
        anomaly_percentage,
        metrics,
    ):
        self.algorithm_name = algorithm_name
        self.algorithm_parameters = algorithm_parameters
        self.dataset_name = dataset_name
        self.num_examples = num_examples
        self.num_dims = num_dims
        self.anomaly_percentage = anomaly_percentage
        self.metrics = metrics

    def __str__(self):
        return (
            f"{self.algorithm_name},{self.dataset_name},"
            f"{self.num_examples},{self.num_dims},{self.anomaly_percentage},"
            f"{self.metrics['time']},{self.metrics['se']},{self.metrics['sp']},"
            f"{self.metrics['p']},{self.metrics['roc']},{self.algorithm_parameters}"
        )
