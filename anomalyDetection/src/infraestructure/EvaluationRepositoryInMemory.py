from domain.interfaces.EvaluationRepository import EvaluationRepository
from domain.models.AlgorithmEvaluationMetrics import AlgorithmEvaluationMetrics


class EvaluationRepositoryInMemory(EvaluationRepository):
    def __init__(self):
        self.metrics = []

    def save(self, metrics: AlgorithmEvaluationMetrics):
        print(metrics)
        self.metrics.append(metrics)

    def printAll(self):
        for metric in self.metrics:
            print(metric)
