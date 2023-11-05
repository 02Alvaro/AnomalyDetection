from domain.interfaces.AlgorithmData import AlgorithmData


class ExecuterNotFound(Exception):
    def __init__(self, algorithm: AlgorithmData):
        message = f"Executer for '{algorithm.__class__.__name__}' not found"
        super().__init__(message)
