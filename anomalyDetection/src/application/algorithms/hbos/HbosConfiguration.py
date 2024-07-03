from dataclasses import dataclass

from application.factories.AlgorithmFactory import AlgorithmFactory
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


@dataclass
@AlgorithmFactory.Configurator_for("hbos")
class HbosConfiguration(AlgorithmConfigurator):
    """
    Configuration class for the HBOS algorithm.

    Attributes
    ----------
    contamination : float
        The amount of contamination of the data set, i.e., the proportion of outliers in the data set. Defaults to 0.1.
    n_bins : int
        Number of bins to use for the histogram. Defaults to 10.
    alpha : float
        Regularizer parameter to prevent overfitting. Defaults to 0.1.
    tol : float
        Tolerance for the binning process. Defaults to 0.5.
    """
    contamination: float = 0.1
    n_bins: int = 10
    alpha: float = 0.1
    tol: float = 0.5
