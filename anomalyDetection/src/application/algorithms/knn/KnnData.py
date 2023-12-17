from dataclasses import dataclass

from application.factories.AlgorithmDataFactory import AlgorithmDataFactory
from domain.interfaces.AlgorithmData import AlgorithmData


@dataclass
@AlgorithmDataFactory.dataClass_for("knn")
class KnnData(AlgorithmData):
    contamination: float = 0.5
    n_neighbors: int = 5
    method: str = "fast"
    radius: float = 1.0
    algorithm: str = "auto"
    leaf_size: int = 30
    metric = "minkowski"
    p: int = 2
    metric_params = None
    n_jobs: int = 1
    target_variable: str = "final_result"
    random_state: int = 42
