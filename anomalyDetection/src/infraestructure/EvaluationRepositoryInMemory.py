from domain.interfaces.EvaluationRepository import EvaluationRepository
from domain.models.AlgorithmEvaluationMetrics import AlgorithmEvaluationMetrics


class EvaluationRepositoryInMemory(EvaluationRepository):
    def save(self, metrics: AlgorithmEvaluationMetrics):
        with open("/app/metrics/all_results.csv", "a") as f:
            f.write(str(metrics) + "\n")
