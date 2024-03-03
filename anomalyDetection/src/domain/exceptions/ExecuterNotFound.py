from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


class ExecuterNotFound(Exception):
    def __init__(self, algorithm: AlgorithmConfigurator):
        message = f"Executer for '{algorithm.__class__.__name__}' not found"
        super().__init__(message)
