from dataclasses import dataclass

from application.factories.AlgorithmFactory import AlgorithmFactory
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


@dataclass
@AlgorithmFactory.Configurator_for("lof")
class LofConfiguration(AlgorithmConfigurator):
    """
    Configuration class for the LOF algorithm.

    Attributes
    ----------
    n_neighbors : int
        Number of neighbors to use. Defaults to 20.
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
    contamination : float
        The amount of contamination of the data set, i.e., the proportion of outliers in the data set. Defaults to 0.1.
    n_jobs : int
        The number of parallel jobs to run for neighbors search. Defaults to 1.
    novelty : bool
        Whether to use LOF for novelty detection. Defaults to True.
    """
    n_neighbors: int = 20
    algorithm: str = "auto"
    leaf_size: int = 30
    metric: str = "minkowski"
    p: int = 2
    metric_params = None
    contamination: float = 0.1
    n_jobs: int = 1
    novelty: bool = True
