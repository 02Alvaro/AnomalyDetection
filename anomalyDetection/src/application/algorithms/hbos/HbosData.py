from dataclasses import dataclass

from application.factories.AlgorithmDataFactory import AlgorithmDataFactory
from domain.interfaces.AlgorithmData import AlgorithmData


@dataclass
@AlgorithmDataFactory.dataClass_for("hbos")
class HbosData(AlgorithmData):
    contamination: float = 0.1
    n_bins: int = 10
    alpha: float = 0.1
    tol: float = 0.5
    target_variable: str = None
    random_state: int = None
