from dataclasses import dataclass

from application.factories.AlgorithmDataFactory import AlgorithmDataFactory
from domain.interfaces.AlgorithmData import AlgorithmData


@dataclass
@AlgorithmDataFactory.dataClass_for("lof")
class LofData(AlgorithmData):
    n_neighbors: int = 20
    algorithm: str = "auto"
    leaf_size: int = 30
    metric: str = "minkowski"
    p: int = 2
    metric_params = None
    contamination: float = 0.1
    n_jobs: int = 1
    novelty: bool = True
    tarjet_variable: str = None
    random_state: int = None
