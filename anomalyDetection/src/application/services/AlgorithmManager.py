from domain.exceptions.ExecuterNotFound import ExecuterNotFound
from domain.exceptions.TrainerNotFound import TrainerNotFound
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator
from domain.interfaces.AlgorithmEvaluate import AlgorithmEvaluate
from domain.interfaces.AlgorithmTrainer import AlgorithmTrainer


class AlgorithmManager:
    executors = {}
    trainers = {}

    @staticmethod
    def evaluator_for(target_class: AlgorithmEvaluate):
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
    def evaluate(algorithm: AlgorithmConfigurator):
        executor_class: AlgorithmEvaluate = AlgorithmManager.executors.get(
            algorithm.__class__
        )
        if not executor_class:
            raise ExecuterNotFound(algorithm)

        algorithm_executor: AlgorithmEvaluate = executor_class()
        algorithm_executor.evaluate(algorithm)

    @staticmethod
    def train(algorithm: AlgorithmConfigurator):
        trainer_class: AlgorithmTrainer = AlgorithmManager.trainers.get(
            algorithm.__class__
        )
        if not trainer_class:
            raise TrainerNotFound(algorithm)

        algorithm_trainer: AlgorithmTrainer = trainer_class()
        algorithm_trainer.train(algorithm)
