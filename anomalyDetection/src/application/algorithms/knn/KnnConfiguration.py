from dataclasses import dataclass

from application.factories.AlgorithmFactory import AlgorithmFactory
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


@dataclass
@AlgorithmFactory.Configurator_for("knn")
class KnnConfiguration(AlgorithmConfigurator):
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
