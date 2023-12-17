import os
from dataclasses import asdict

import pandas as pd
from application.algorithms.dae.DaeData import DaeData
from application.services.AlgorithmManager import AlgorithmManager
from application.services.TimeEvalWrapper import TimeEvalParameters, TimeEvalWrapper
from application.utils.datapaths import (
    DATA_PATH_DOCKER,
    DATA_PATH_HOST,
    RESULTS_PATH_DOCKER,
    RESULTS_PATH_HOST,
)
from domain.interfaces.AlgorithmExecutor import AlgorithmExecutor
from domain.interfaces.EvaluationRepository import EvaluationRepository
from domain.services.metrics import performance_metrics


@AlgorithmManager.executor_for(DaeData)
class DaeExecutor(AlgorithmExecutor):
    def __init__(self, repository: EvaluationRepository, time_eval: TimeEvalWrapper):
        self.time_eval = time_eval
        self.repositoy = repository

    def execute(self, command: DaeData):
        self.executeAlgorithm(command)
        self.evaluate_performance(
            command.data_file, os.path.join(RESULTS_PATH_DOCKER, "anomaly_scores.ts")
        )

    def executeAlgorithm(self, command: DaeData):
        param_dict = asdict(command)
        del param_dict["data_file"]

        time_eval_parameters = TimeEvalParameters(
            name="dae",
            execution_type="train",
            data_input=command.data_file,
            parameters=param_dict,
        )

        self.time_eval.execute(time_eval_parameters)
        time_eval_parameters = TimeEvalParameters(
            name="dae",
            execution_type="execute",
            data_input=command.data_file,
            parameters=param_dict,
        )
        self.time_eval.execute(time_eval_parameters)

    def evaluate_performance(self, original_file, result_file):
        file = os.path.join(DATA_PATH_DOCKER, original_file)
        result_file = os.path.join(RESULTS_PATH_DOCKER, result_file)
        anomaly_scores = pd.read_csv(result_file)
        original_data = pd.read_csv(file)

        threshold = 0.5
        anomaly_scores["binarized_scores"] = [
            1 if x > threshold else 0 for x in anomaly_scores.iloc[:, 0]
        ]

        is_anomaly = original_data["is_anomaly"]
        is_anomaly = is_anomaly[1:]

        metrics = performance_metrics(is_anomaly, anomaly_scores["binarized_scores"])

        print(metrics)

        return metrics
