import os
from dataclasses import asdict

import pandas as pd
from anomalyDetection.gateway.Algorithms.autoencoder.AutoEncoderCommand import (
    AutoEncoderCommand,
)
from anomalyDetection.gateway.CommandPattern.CommandHandler import CommandHandler
from anomalyDetection.gateway.utils.datapaths import (
    DATA_PATH,
    DATA_PATH_DOCKER,
    RESULTS_PATH,
    RESULTS_PATH_DOCKER,
)
from anomalyDetection.gateway.utils.TimeEvalWrapper import (
    TimeEvalParameters,
    TimeEvalWrapper,
)

from anomalyDetection.anomalyDetection import performance_metrics


class AutoEncoderCommandHandler(CommandHandler):
    def __init__(self) -> None:
        self.time_eval_wrapper = TimeEvalWrapper(DATA_PATH, RESULTS_PATH)

    def execute(self, command: AutoEncoderCommand):
        self.executeAlgorithm(command)
        self.evaluate_performance(
            command.filePath, os.path.join(RESULTS_PATH_DOCKER, "anomaly_scores.ts")
        )

    def executeAlgorithm(self, command: AutoEncoderCommand):
        param_dict = asdict(command)
        del param_dict["filePath"]

        time_eval_parameters = TimeEvalParameters(
            name="autoencoder",
            execution_type="execute",
            data_input=command.filePath,
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
