import os
from dataclasses import asdict

import pandas as pd
from application.utils.datapaths import DATA_PATH_DOCKER
from domain.interfaces.AlgorithmData import AlgorithmData
from domain.interfaces.EvaluationRepository import EvaluationRepository
from domain.models.AlgorithmEvaluationMetrics import AlgorithmEvaluationMetrics
from domain.services.metrics import file_data, performance_metrics


class AlgorithmDataProcesor:
    def process(
        self, algorithm_data: AlgorithmData, prediction_data: pd.DataFrame, time: int
    ) -> AlgorithmEvaluationMetrics:
        try:
            target_variable = algorithm_data.target_variable
        except AttributeError:
            target_variable = "is_anomaly"

        file = os.path.join(DATA_PATH_DOCKER, algorithm_data.data_file)
        original_data = pd.read_csv(file)[target_variable]
        original_data = original_data[1:]
        metrics = performance_metrics(
            original_data, prediction_data.round().astype(int)
        )
        metrics["time"] = time

        file_info = file_data(algorithm_data.data_file)

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

        return algorithm_evaluation_metrics
