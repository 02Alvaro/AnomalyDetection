from dataclasses import dataclass

from application.factories.AlgorithmFactory import AlgorithmFactory
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


@dataclass
@AlgorithmFactory.Configurator_for("autoencoder")
class AutoEncoderConfiguration(AlgorithmConfigurator):
    """
    Configuration class for the AutoEncoder algorithm.

    Attributes:
        latent_size (int): The size of the latent space. Defaults to 32.
        epochs (int): The number of epochs to train the autoencoder. Defaults to 100.
        learning_rate (float): The learning rate for the optimizer. Defaults to 0.005.
        early_stopping_delta (float): Minimum change to qualify as an improvement for early stopping. Defaults to 1e-2.
        early_stopping_patience (int): Number of epochs with no improvement after which training will be stopped. Defaults to 10.
        split (float): The fraction of the dataset to be used for training. Defaults to 0.8.
    """
    latent_size: int = 32
    epochs: int = 100
    learning_rate: float = 0.005
    early_stopping_delta: float = 1e-2
    early_stopping_patience: int = 10
    split: float = 0.8
