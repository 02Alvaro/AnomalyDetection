from dataclasses import dataclass

from application.factories.AlgorithmFactory import AlgorithmFactory
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


@dataclass
@AlgorithmFactory.Configurator_for("hbos")
class HbosConfiguration(AlgorithmConfigurator):
    contamination: float = 0.1
    n_bins: int = 10
    alpha: float = 0.1
    tol: float = 0.5
