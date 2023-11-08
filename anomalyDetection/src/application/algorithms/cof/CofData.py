from dataclasses import dataclass

from application.factories.AlgorithmDataFactory import AlgorithmDataFactory
from domain.interfaces.AlgorithmData import AlgorithmData


@dataclass
@AlgorithmDataFactory.dataClass_for("cof")
class CofData(AlgorithmData):
    contamination: float = 0.1
    n_neighbors: int = 20
    method: str = "fast"
    random_state: int = 42
    tarjet_variable: str = "final_result"
