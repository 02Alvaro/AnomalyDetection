import os

from domain.interfaces.EvaluationRepository import EvaluationRepository
from domain.models.AlgorithmEvaluationMetrics import AlgorithmEvaluationMetrics


class EvaluationRepositoryInFile(EvaluationRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(
        self, metrics: AlgorithmEvaluationMetrics, filename: str = "all_results.csv"
    ):
        header = "Algorithm,dataset,samples,dims,anomaly_rate,time,se,sp,p,roc,params\n"
        file_path = os.path.join(self.file_path, filename)

        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(header)

        with open(file_path, "a") as f:
            f.write(str(metrics) + "\n")
        print(metrics)
