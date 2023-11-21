from abc import abstractmethod

from domain.models.AlgorithmEvaluationMetrics import AlgorithmEvaluationMetrics


class EvaluationRepository:
    @abstractmethod
    def save(metrics: AlgorithmEvaluationMetrics):
        pass
