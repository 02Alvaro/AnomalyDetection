from domain.exceptions.ExecuterNotFound import ExecuterNotFound
from domain.exceptions.TrainerNotFound import TrainerNotFound
from domain.interfaces.AlgorithmData import AlgorithmData
from domain.interfaces.AlgorithmExecutor import AlgorithmExecutor
from domain.interfaces.AlgorithmTrainer import AlgorithmTrainer


class AlgorithmManager:
    executors = {}
    trainers = {}

    @staticmethod
    def executor_for(target_class: AlgorithmExecutor):
        def decorator(cls):
            AlgorithmManager.executors[target_class] = cls
            return cls

        return decorator

    @staticmethod
    def trainer_for(target_class: AlgorithmTrainer):
        def decorator(cls):
            AlgorithmManager.trainers[target_class] = cls
            return cls

        return decorator

    @staticmethod
    def execute(algorithm: AlgorithmData):
        executor_class: AlgorithmExecutor = AlgorithmManager.executors.get(
            algorithm.__class__
        )
        if not executor_class:
            raise ExecuterNotFound(algorithm)

        algorithm_executor = executor_class()
        algorithm_executor.execute(algorithm)

    @staticmethod
    def train(algorithm: AlgorithmData):
        trainer_class: AlgorithmTrainer = AlgorithmManager.trainers.get(
            algorithm.__class__
        )
        if not trainer_class:
            raise TrainerNotFound(algorithm)

        algorithm_trainer = trainer_class()
        algorithm_trainer.train(algorithm)
