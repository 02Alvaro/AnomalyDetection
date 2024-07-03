from dataclasses import dataclass

from application.factories.AlgorithmFactory import AlgorithmFactory
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


@dataclass
@AlgorithmFactory.Configurator_for("lstmvae")
class LstmVaeConfiguration(AlgorithmConfigurator):
    """
    Configuration class for the LSTM-VAE algorithm.

    Attributes
    ----------
    learning_rate : float
        The learning rate for the optimizer. Defaults to 0.001.
    epochs : int
        The number of epochs to train the model. Defaults to 10.
    batch_size : int
        The size of the training batches. Defaults to 32.
    window_size : int
        The size of the input window. Defaults to 10.
    latent_size : int
        The size of the latent space. Defaults to 5.
    lstm_layers : int
        The number of LSTM layers. Defaults to 10.
    rnn_hidden_size : int
        The size of the hidden state in the RNN. Defaults to 5.
    early_stopping_delta : float
        Minimum change to qualify as an improvement for early stopping. Defaults to 0.05.
    early_stopping_patience : int
        Number of epochs with no improvement after which training will be stopped. Defaults to 10.
    """
    learning_rate: float = 0.001
    epochs: int = 10
    batch_size: int = 32
    window_size: int = 10
    latent_size: int = 5
    lstm_layers: int = 10
    rnn_hidden_size: int = 5
    early_stopping_delta: float = 0.05
    early_stopping_patience: int = 10
