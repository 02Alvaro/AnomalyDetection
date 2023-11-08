import os
from dataclasses import asdict

import pandas as pd
from application.algorithms.lstmVae.LstmVaeData import LstmVaeData
from application.services.AlgorithmManager import AlgorithmManager
from application.services.TimeEvalWrapper import TimeEvalParameters, TimeEvalWrapper
from application.utils.datapaths import (
    DATA_PATH,
    DATA_PATH_DOCKER,
    RESULTS_PATH,
    RESULTS_PATH_DOCKER,
)
from domain.interfaces.AlgorithmExecutor import AlgorithmExecutor
from domain.services.metrics import performance_metrics


@AlgorithmManager.executor_for(LstmVaeData)
class LstmVaeExecutor(AlgorithmExecutor):
    def __init__(self) -> None:
        self.time_eval_wrapper = TimeEvalWrapper(DATA_PATH, RESULTS_PATH)

    def execute(self, command: LstmVaeData):
        self.executeAlgorithm(command)
        self.evaluate_performance(
            command.file_path, os.path.join(RESULTS_PATH_DOCKER, "anomaly_scores.ts")
        )

    def executeAlgorithm(self, command: LstmVaeData):
        param_dict = asdict(command)
        del param_dict["file_path"]

        time_eval_parameters = TimeEvalParameters(
            name="lstm_vae",
            execution_type="train",
            data_input=command.file_path,
            parameters=param_dict,
        )

        self.time_eval_wrapper.execute(time_eval_parameters)
        time_eval_parameters = TimeEvalParameters(
            name="lstm_vae",
            execution_type="execute",
            data_input=command.file_path,
            parameters=param_dict,
        )

        self.time_eval_wrapper.execute(time_eval_parameters)

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
