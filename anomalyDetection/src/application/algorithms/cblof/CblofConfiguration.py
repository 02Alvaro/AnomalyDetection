from dataclasses import dataclass

from application.factories.AlgorithmFactory import AlgorithmFactory
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


@dataclass
@AlgorithmFactory.Configurator_for("cblof")
class CblofConfiguration(AlgorithmConfigurator):
    """
    Configuration class for the CBLOF algorithm.

    Attributes
    ----------
    n_clusters : int
        Number of clusters to form. Defaults to 100.
    contamination : float
        The amount of contamination of the data set, i.e., the proportion of outliers in the data set. Defaults to 0.1.
    clustering_estimator : 
        The base clustering algorithm to use. Defaults to None.
    alpha : float
        Weight factor for small clusters. Defaults to 0.9.
    beta : float
        Weight factor for large clusters. Defaults to 5.
    use_weights : bool
        Whether to use weights for the clusters. Defaults to False.
    check_estimator : bool
        Whether to check the estimator's parameters. Defaults to False.
    """
    n_clusters: int = 100
    contamination: float = 0.1
    clustering_estimator = None
    alpha: float = 0.9
    beta: float = 5
    use_weights: bool = False
    check_estimator: bool = False
