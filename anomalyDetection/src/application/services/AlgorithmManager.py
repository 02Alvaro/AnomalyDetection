from domain.exceptions.ExecuterNotFound import ExecuterNotFound
from domain.interfaces.AlgorithmData import AlgorithmData
from domain.interfaces.AlgorithmExecutor import AlgorithmExecutor


class AlgorithmManager:
    executors = {}

    @staticmethod
    def executor_for(target_class: AlgorithmExecutor):
        def decorator(cls):
            AlgorithmManager.executors[target_class] = cls
            return cls

        return decorator

    def execute(algorithm: AlgorithmData):
        executor_class: AlgorithmExecutor = AlgorithmManager.executors.get(
            algorithm.__class__
        )
        if not executor_class:
            raise ExecuterNotFound(algorithm)

        algorithm_executor = executor_class()
        algorithm_executor.execute(algorithm)
