from dataclasses import dataclass

from anomalyDetection.gateway.CommandPattern.Command import Command


@dataclass
class DaeCommand(Command):
    filePath: str
    latent_size: int = 32
    epochs: int = 10
    learning_rate: float = 0.005
    noise_ratio: float = 0.1
    split: float = 0.8
    early_stopping_delta: float = 1e-2
    early_stopping_patience: int = 10
    random_state: int = 42
