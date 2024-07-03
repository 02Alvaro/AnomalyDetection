from dataclasses import dataclass

from application.factories.AlgorithmFactory import AlgorithmFactory
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


@dataclass
@AlgorithmFactory.Configurator_for("cof")
class CofConfigurator(AlgorithmConfigurator):
    """
    Configuration class for the COF algorithm.

    Attributes
    ----------
    contamination : float
        The amount of contamination of the data set, i.e., the proportion of outliers in the data set. Defaults to 0.1.
    n_neighbors : int
        Number of neighbors to use. Defaults to 20.
    method : str
        Method to use for the COF algorithm. Defaults to "fast".
    """
    contamination: float = 0.1
    n_neighbors: int = 20
    method: str = "fast"
