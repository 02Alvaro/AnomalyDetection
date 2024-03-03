from dataclasses import dataclass

from application.factories.AlgorithmFactory import AlgorithmFactory
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


@dataclass
@AlgorithmFactory.Configurator_for("cblof")
class CblofConfiguration(AlgorithmConfigurator):
    n_clusters: int = 8
    contamination: float = 0.1
    clustering_estimator = None
    alpha: float = 0.9
    beta: float = 5
    use_weights: bool = False
    check_estimator: bool = False
