from domain.interfaces.EvaluationRepository import EvaluationRepository
from domain.models.AlgorithmEvaluationMetrics import AlgorithmEvaluationMetrics


class EvaluationRepositoryInFile(EvaluationRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, metrics: AlgorithmEvaluationMetrics):
        with open(self.file_path + "/" + "all_results.csv", "a") as f:
            f.write(str(metrics) + "\n")
