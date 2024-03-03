from dataclasses import dataclass

from application.factories.AlgorithmFactory import AlgorithmFactory
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


@dataclass
@AlgorithmFactory.Configurator_for("lof")
class LofConfigurator(AlgorithmConfigurator):
    n_neighbors: int = 20
    algorithm: str = "auto"
    leaf_size: int = 30
    metric: str = "minkowski"
    p: int = 2
    metric_params = None
    contamination: float = 0.1
    n_jobs: int = 1
    novelty: bool = True
