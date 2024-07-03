from domain.exceptions.ExecuterNotFound import ExecuterNotFound
from domain.exceptions.TrainerNotFound import TrainerNotFound
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator
from domain.interfaces.AlgorithmEvaluate import AlgorithmEvaluate
from domain.interfaces.AlgorithmTrainer import AlgorithmTrainer


class AlgorithmManager:
    """
    Manager class for handling algorithm executors and trainers.

    Attributes
    ----------
    executors : dict
        Dictionary mapping target classes to their respective executor classes.
    trainers : dict
        Dictionary mapping target classes to their respective trainer classes.
    """
    executors = {}
    trainers = {}

    @staticmethod
    def evaluator_for(target_class: AlgorithmEvaluate):
        """
        Decorator for registering an algorithm evaluator.

        Parameters
        ----------
        target_class : AlgorithmEvaluate
            The target class to be evaluated.

        Returns
        -------
        function
            A decorator function that registers the evaluator class in the executors dictionary.
        """
        def decorator(cls):
            AlgorithmManager.executors[target_class] = cls
            return cls

        return decorator

    @staticmethod
    def trainer_for(target_class: AlgorithmTrainer):
        """
        Decorator for registering an algorithm trainer.

        Parameters
        ----------
        target_class : AlgorithmTrainer
            The target class to be trained.

        Returns
        -------
        function
            A decorator function that registers the trainer class in the trainers dictionary.
        """
        def decorator(cls):
            AlgorithmManager.trainers[target_class] = cls
            return cls

        return decorator

    @staticmethod
    def evaluate(algorithm: AlgorithmConfigurator):
        """
        Evaluates the given algorithm using the registered evaluator.

        Parameters
        ----------
        algorithm : AlgorithmConfigurator
            The algorithm configuration to be evaluated.

        Raises
        ------
        ExecuterNotFound
            If no executor is found for the given algorithm class.
        """
        executor_class: AlgorithmEvaluate = AlgorithmManager.executors.get(
            algorithm.__class__
        )
        if not executor_class:
            raise ExecuterNotFound(algorithm)

        algorithm_executor: AlgorithmEvaluate = executor_class()
        algorithm_executor.evaluate(algorithm)

    @staticmethod
    def train(algorithm: AlgorithmConfigurator):
        """
        Trains the given algorithm using the registered trainer.

        Parameters
        ----------
        algorithm : AlgorithmConfigurator
            The algorithm configuration to be trained.

        Raises
        ------
        TrainerNotFound
            If no trainer is found for the given algorithm class.
        """
        trainer_class: AlgorithmTrainer = AlgorithmManager.trainers.get(
            algorithm.__class__
        )
        if not trainer_class:
            raise TrainerNotFound(algorithm)

        algorithm_trainer: AlgorithmTrainer = trainer_class()
        algorithm_trainer.train(algorithm)
