from domain.interfaces.AlgorithmData import AlgorithmData


class TrainerNotFound(Exception):
    def __init__(self, algorithm: AlgorithmData):
        message = f"Trainer for '{algorithm.__class__.__name__}' not found"
        super().__init__(message)
