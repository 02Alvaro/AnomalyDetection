import json
from dataclasses import dataclass, field

from application.services.DockerExecutor import DockerExecutor


@dataclass
class TimeEvalParameters:
    name: str = "lstm_vae"
    execution_type: str = "execute"
    data_input: str = "dataset.csv"
    data_output: str = "anomaly_scores.ts"
    model_input: str = "model.pkl"
    model_output: str = "model.pkl"
    parameters: dict = field(default_factory=dict)


class TimeEvalWrapper:
    def __init__(self, data_path: str, results_path: str):
        self.data_path = data_path
        self.results_path = results_path

    def _build_docker_command(self, algorithm: TimeEvalParameters) -> str:
        return (
            f"docker run --rm "
            f"-v {self.data_path}:/data:ro "
            f"-v {self.results_path}:/results:rw "
            f"registry.gitlab.hpi.de/akita/i/{algorithm.name}:latest execute-algorithm "
            f'\'{{"executionType": "{algorithm.execution_type}", "dataInput": "/data/{algorithm.data_input}", '
            f'"dataOutput": "/results/{algorithm.data_output}", "modelInput": "/results/{algorithm.model_input}", '
            f'"modelOutput": "/results/{algorithm.model_output}", "customParameters": {json.dumps(algorithm.parameters)}}}\''
        )

    def execute(self, algorithm: TimeEvalParameters):
        docker_command_str = self._build_docker_command(algorithm)
        DockerExecutor.execute(docker_command_str)

    def create_image(self, algorithm_name):
        docker_command_str = (
            f"docker build -t registry.gitlab.hpi.de/akita/i/{algorithm_name}:latest ."
        )
        DockerExecutor().execute(docker_command_str)
