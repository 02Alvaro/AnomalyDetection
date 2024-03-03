from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


class TrainerNotFound(Exception):
    def __init__(self, algorithm: AlgorithmConfigurator):
        message = f"Trainer for '{algorithm.__class__.__name__}' not found"
        super().__init__(message)
