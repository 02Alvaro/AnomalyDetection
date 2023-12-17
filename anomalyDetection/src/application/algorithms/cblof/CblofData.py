from dataclasses import dataclass

from application.factories.AlgorithmDataFactory import AlgorithmDataFactory
from domain.interfaces.AlgorithmData import AlgorithmData


@dataclass
@AlgorithmDataFactory.dataClass_for("cblof")
class CblofData(AlgorithmData):
    n_clusters: int = 8
    contamination: float = 0.1
    clustering_estimator = None
    alpha: float = 0.9
    beta: float = 5
    use_weights: bool = False
    check_estimator: bool = False
    random_state: int = None
    target_variable: str = None
