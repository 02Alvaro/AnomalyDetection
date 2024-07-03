from dataclasses import dataclass

from application.factories.AlgorithmFactory import AlgorithmFactory
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


@dataclass
@AlgorithmFactory.Configurator_for("knn")
class KnnConfiguration(AlgorithmConfigurator):
    """
    Configuration class for the KNN algorithm.

    Attributes
    ----------
    contamination : float
        The amount of contamination of the data set, i.e., the proportion of outliers in the data set. Defaults to 0.5.
    n_neighbors : int
        Number of neighbors to use. Defaults to 5.
    method : str
        Method to use for the KNN algorithm. Defaults to "fast".
    radius : float
        Radius of the neighborhood for the KNN algorithm. Defaults to 1.0.
    algorithm : str
        Algorithm to use for computing the nearest neighbors. Defaults to "auto".
    leaf_size : int
        Leaf size passed to BallTree or KDTree. Defaults to 30.
    metric : str
        The distance metric to use for the tree. Defaults to "minkowski".
    p : int
        Power parameter for the Minkowski metric. Defaults to 2.
    metric_params : dict, optional
        Additional keyword arguments for the metric function. Defaults to None.
    n_jobs : int
        The number of parallel jobs to run for neighbors search. Defaults to 1.
    """
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
