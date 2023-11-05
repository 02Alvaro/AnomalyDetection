class AlgorithmDataNotFound(Exception):
    def __init__(self, name: str):
        message = f"AlgorithmData for '{name}' not found"
        super().__init__(message)
