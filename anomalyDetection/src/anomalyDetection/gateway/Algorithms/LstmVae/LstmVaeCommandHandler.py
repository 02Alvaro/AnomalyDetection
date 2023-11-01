import json
import os
from dataclasses import asdict

import pandas as pd
from anomalyDetection.gateway.Algorithms.LstmVae.LstmVaeCommand import LstmVaeCommand
from anomalyDetection.gateway.CommandPattern.CommandHandler import CommandHandler
from anomalyDetection.gateway.utils.TimeEvalWrapper import (
    TimeEvalParameters,
    TimeEvalWrapper,
)

from anomalyDetection.anomalyDetection import performance_metrics

DATA_PATH = "E:/TFG/anomalyDetection/src/TimeEval-algorithms-main/1-data"
DATA_PATH_DOCKER = "/app/src/TimeEval-algorithms-main/1-data"
RESULTS_PATH = "E:/TFG/anomalyDetection/src/TimeEval-algorithms-main/2-results"
RESULTS_PATH_DOCKER = "/app/src/TimeEval-algorithms-main/2-results"


class LstmVaeCommandHandler(CommandHandler):
    def __init__(self) -> None:
        self.time_eval_wrapper = TimeEvalWrapper(DATA_PATH, RESULTS_PATH)

    def execute(self, command: LstmVaeCommand):
        self.executeAlgorithm(command)
        self.evaluate_performance(
            command.filePath, os.path.join(RESULTS_PATH_DOCKER, "anomaly_scores.ts")
        )

    def executeAlgorithm(self, command: LstmVaeCommand):
        param_dict = asdict(command)
        del param_dict["filePath"]

        time_eval_parameters = TimeEvalParameters(
            name="lstm_vae",
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
        anomaly_scores["binarized_scores"] = [
            1 if x > threshold else 0 for x in anomaly_scores.iloc[:, 0]
        ]

        is_anomaly = original_data["is_anomaly"]
        is_anomaly = is_anomaly[1:]

        metrics = performance_metrics(is_anomaly, anomaly_scores["binarized_scores"])

        print(metrics)

        return metrics
