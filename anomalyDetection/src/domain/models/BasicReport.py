from dataclasses import dataclass


@dataclass
class BasicReport:
    """
    Class for storing and displaying basic algorithm evaluation reports.

    Attributes
    ----------
    algorithm_name : str
        The name of the algorithm.
    model : str
        The name of the model.
    dataset_name : str
        The name of the dataset.
    num_examples : int
        The number of examples in the dataset.
    num_dims : int
        The number of dimensions in the dataset.
    anomaly_percentage : float
        The percentage of anomalies in the dataset.
    metrics : dict
        A dictionary containing evaluation metrics.
    """

    algorithm_name: str
    model: str
    dataset_name: str
    num_examples: int
    num_dims: int
    anomaly_percentage: float
    metrics: dict

    def __init__(
        self,
        algorithm_name,
        model,
        dataset_name,
        num_examples,
        num_dims,
        anomaly_percentage,
        metrics,
    ):
        """
        Initializes the BasicReport with the given parameters.

        Parameters
        ----------
        algorithm_name : str
            The name of the algorithm.
        model : str
            The name of the model.
        dataset_name : str
            The name of the dataset.
        num_examples : int
            The number of examples in the dataset.
        num_dims : int
            The number of dimensions in the dataset.
        anomaly_percentage : float
            The percentage of anomalies in the dataset.
        metrics : dict
            A dictionary containing evaluation metrics.
        """
        self.algorithm_name = algorithm_name
        self.model = model
        self.dataset_name = dataset_name
        self.num_examples = num_examples
        self.num_dims = num_dims
        self.anomaly_percentage = anomaly_percentage
        self.metrics = metrics

    def __str__(self):
        """
        Returns a string representation of the BasicReport.

        Returns
        -------
        str
            A string containing the basic report details.
        """
        return (
            f"{self.algorithm_name},{self.model},{self.dataset_name},"
            f"{self.num_examples},{self.num_dims},{self.anomaly_percentage},"
            f"{self.metrics['time']},{self.metrics['se']},{self.metrics['sp']},"
            f"{self.metrics['p']},{self.metrics['roc']}"
        )
