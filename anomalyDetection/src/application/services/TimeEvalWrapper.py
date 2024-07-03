import json
from dataclasses import dataclass, field

from application.services.DockerExecutor import DockerExecutor


@dataclass
class TimeEvalParameters:
    """
    Data class for storing parameters related to TimeEval execution.

    Attributes
    ----------
    name : str
        The name of the algorithm. Defaults to "lstm_vae".
    execution_type : str
        The type of execution (e.g., "execute", "train"). Defaults to "execute".
    data_input : str
        The input data file. Defaults to "dataset.csv".
    data_output : str
        The output data file. Defaults to "anomaly_scores.ts".
    model_input : str
        The input model file. Defaults to "model.pkl".
    model_output : str
        The output model file. Defaults to "model.pkl".
    parameters : dict
        Additional parameters for the execution. Defaults to an empty dictionary.
    """
    name: str = "lstm_vae"
    execution_type: str = "execute"
    data_input: str = "dataset.csv"
    data_output: str = "anomaly_scores.ts"
    model_input: str = "model.pkl"
    model_output: str = "model.pkl"
    parameters: dict = field(default_factory=dict)


class TimeEvalWrapper:
    """
    Wrapper class for executing TimeEval operations using Docker.

    Attributes
    ----------
    data_path : str
        The path to the data directory.
    results_path : str
        The path to the results directory.
    """

    def __init__(self, data_path: str, results_path: str):
        """
        Initializes the TimeEvalWrapper with the provided data and results paths.

        Parameters
        ----------
        data_path : str
            The path to the data directory.
        results_path : str
            The path to the results directory.
        """
        self.data_path = data_path
        self.results_path = results_path

    def _build_docker_command(self, algorithm: TimeEvalParameters) -> str:
        """
        Builds the Docker command string for the given algorithm parameters.

        Parameters
        ----------
        algorithm : TimeEvalParameters
            The parameters for the algorithm execution.

        Returns
        -------
        str
            The Docker command string.
        """
        return (
            f"docker run --rm "
            f"-v {self.data_path}:/data:ro "
            f"-v {self.results_path}:/results:rw "
            f"ghcr.io/timeeval/{algorithm.name}:latest execute-algorithm "
            f'\'{{"executionType": "{algorithm.execution_type}", "dataInput": "/data/{algorithm.data_input}", '
            f'"dataOutput": "/results/{algorithm.data_output}", "modelInput": "/results/{algorithm.model_input}", '
            f'"modelOutput": "/results/{algorithm.model_output}", "customParameters": {json.dumps(algorithm.parameters)}}}\''
        )

    def execute(self, algorithm: TimeEvalParameters):
        """
        Executes the given algorithm using Docker.

        Parameters
        ----------
        algorithm : TimeEvalParameters
            The parameters for the algorithm execution.
        """
        docker_command_str = self._build_docker_command(algorithm)
        DockerExecutor.execute(docker_command_str)

    def create_image(self, algorithm_name):
        """
        Creates a Docker image for the given algorithm.

        Parameters
        ----------
        algorithm_name : str
            The name of the algorithm.
        """
        docker_command_str = (
            f"docker build -t ghcr.io/timeeval/{algorithm_name}:latest ."
        )
        DockerExecutor().execute(docker_command_str)
