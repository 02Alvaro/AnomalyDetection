import os
from dataclasses import asdict

import pandas as pd
from application.algorithms.autoencoder.AutoEncoderData import AutoEncoderData
from application.services.AlgorithmManager import AlgorithmManager
from application.services.TimeEvalWrapper import TimeEvalParameters, TimeEvalWrapper
from application.utils.datapaths import (
    DATA_PATH_DOCKER,
    DATA_PATH_HOST,
    RESULTS_PATH_DOCKER,
    RESULTS_PATH_HOST,
)
from domain.interfaces.AlgorithmExecutor import AlgorithmExecutor
from domain.services.metrics import performance_metrics
from inject import Inject


@AlgorithmManager.executor_for(AutoEncoderData)
class AutoEncoderExecutor(AlgorithmExecutor):
    @Inject
    def __init__(self,) -> None:
        self.time_eval_wrapper = TimeEvalWrapper(DATA_PATH_HOST, RESULTS_PATH_HOST)

    def execute(self, command: AutoEncoderData):
        self.executeAlgorithm(command)
        self.evaluate_performance(
            command.data_file, os.path.join(RESULTS_PATH_DOCKER, "anomaly_scores.ts")
        )

    def executeAlgorithm(self, command: AutoEncoderData):
        param_dict = asdict(command)
        del param_dict["data_file"]

        time_eval_parameters = TimeEvalParameters(
            name="autoencoder",
            execution_type="train",
            data_input=command.data_file,
            parameters=param_dict,
        )

        self.time_eval_wrapper.execute(time_eval_parameters)
        time_eval_parameters = TimeEvalParameters(
            name="autoencoder",
            execution_type="execute",
            data_input=command.data_file,
            parameters=param_dict,
        )

        self.time_eval_wrapper.execute(time_eval_parameters)

    def evaluate_performance(self, original_file, result_file):
        file = os.path.join(DATA_PATH_DOCKER, original_file)
        result_file = os.path.join(RESULTS_PATH_DOCKER, result_file)
        anomaly_scores = pd.read_csv(result_file)
        original_data = pd.read_csv(file)

        threshold = 0.5
        anomaly_scores.iloc[:, 0] = [
            1 if x > threshold else 0 for x in anomaly_scores.iloc[:, 0]
        ]

        is_anomaly = original_data["is_anomaly"]
        is_anomaly = is_anomaly[1:]

        metrics = performance_metrics(is_anomaly, anomaly_scores.iloc[:, 0])

        print(metrics)

        return metrics
