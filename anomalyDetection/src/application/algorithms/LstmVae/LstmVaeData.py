from dataclasses import dataclass

from application.factories.AlgorithmDataFactory import AlgorithmDataFactory
from domain.interfaces.AlgorithmData import AlgorithmData


@dataclass
@AlgorithmDataFactory.dataClass_for("lstmvae")
class LstmVaeData(AlgorithmData):
    learning_rate: float = 0.001
    epochs: int = 10
    batch_size: int = 32
    window_size: int = 10
    latent_size: int = 5
    lstm_layers: int = 10
    rnn_hidden_size: int = 5
    early_stopping_delta: float = 0.05
    early_stopping_patience: int = 10
