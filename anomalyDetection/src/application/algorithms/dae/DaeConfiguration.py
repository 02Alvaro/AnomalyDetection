from dataclasses import dataclass

from application.factories.AlgorithmFactory import AlgorithmFactory
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


@dataclass
@AlgorithmFactory.Configurator_for("dae")
class DaeConfiguration(AlgorithmConfigurator):
    latent_size: int = 32
    epochs: int = 100
    learning_rate: float = 0.005
    noise_ratio: float = 0.1
    split: float = 0.8
    early_stopping_delta: float = 1e-2
    early_stopping_patience: int = 10
