from dataclasses import dataclass

from application.factories.AlgorithmFactory import AlgorithmFactory
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


@dataclass
@AlgorithmFactory.Configurator_for("cof")
class CofConfigurator(AlgorithmConfigurator):
    contamination: float = 0.1
    n_neighbors: int = 20
    method: str = "fast"
