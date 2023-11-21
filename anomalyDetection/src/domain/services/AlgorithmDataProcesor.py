import os
from dataclasses import asdict

import pandas as pd
from application.utils.datapaths import DATA_PATH_DOCKER
from domain.interfaces.AlgorithmData import AlgorithmData
from domain.interfaces.EvaluationRepository import EvaluationRepository
from domain.models.AlgorithmEvaluationMetrics import AlgorithmEvaluationMetrics
from domain.services.metrics import file_data, performance_metrics


class AlgorithmDataProcesor():
    execution_data = {}

    def __init__(self, repository: EvaluationRepository) -> None:
        self.repositoy = repository

    def process(self, algorithm_data: AlgorithmData, prediction_data):
        file = os.path.join(DATA_PATH_DOCKER, algorithm_data.file_path)
        original_data = pd.read_csv(file)["is_anomaly"]
        metrics = performance_metrics(original_data, prediction_data)
        file_info: {
            "name": str,
            "num_examples": int,
            "num_dims": int,
            "anomaly_percentage": float,
        }
        if algorithm_data.random_state == None:
            file_info = file_data(algorithm_data.file_path)
        else:
            file_info = file_data(algorithm_data.file_path, algorithm_data.random_state)

        algorithm_evaluation_metrics: AlgorithmEvaluationMetrics = (
            AlgorithmEvaluationMetrics(
                algorithm_name=algorithm_data.__class__.__name__.replace("Data", ""),
                algorithm_parameters=asdict(algorithm_data),
                dataset_name=file_info["name"],
                num_examples=file_info["num_examples"],
                num_dims=file_info["num_dims"],
                anomaly_percentage=file_info["anomaly_percentage"],
                metrics=metrics,
            )
        )

        self.repositoy.save(algorithm_evaluation_metrics)
