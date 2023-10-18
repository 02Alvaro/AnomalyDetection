import os
import json
import pandas as pd
from dataclasses import asdict
from anomalyDetection.anomalyDetection import performance_metrics

from anomalyDetection.gateway.Algorithms.LstmVae.LstmVaeCommand import LstmVaeCommand
from anomalyDetection.gateway.Interfaces.CommandHandler import CommandHandler
from anomalyDetection.gateway.utils.DockerExecutor import DockerExecutor

class LstmVaeCommandHandler(CommandHandler):


    def execute(self, command: LstmVaeCommand):
        self.dockerAlgorithm(command)
        self.evaluate_performance(command.filePath, '/app/src/TimeEval-algorithms-main/2-results/anomaly_scores.ts')

    def dockerAlgorithm(self, command: LstmVaeCommand):
        absolute_data_path = "E:/TFG/anomalyDetection/src/TimeEval-algorithms-main/1-data"
        absolute_results_path = "E:/TFG/anomalyDetection/src/TimeEval-algorithms-main/2-results"
        
        dockerChain='docker run --rm -v {data_path}:/data:ro -v {results_path}:/results:rw registry.gitlab.hpi.de/akita/i/lstm_vae:latest execute-algorithm \'{{"executionType": "execute", "dataInput": "/data/{file_name}", "dataOutput": "/results/anomaly_scores.ts", "modelInput": "/results/model.pkl", "modelOutput": "/results/model.pkl", "customParameters": {json_str}}}\''
        json_str = json.dumps(asdict(command))
        print(json_str)
        docker_command_str = dockerChain.format(data_path=absolute_data_path, results_path=absolute_results_path, file_name=command.filePath, json_str=json_str)
        DockerExecutor().execute(docker_command_str)

    def evaluate_performance(self,original_file, result_file ):
        file="/app/src/TimeEval-algorithms-main/1-data/"+original_file
        anomaly_scores = pd.read_csv(result_file)
        original_data = pd.read_csv(file)

        threshold = 0.5
        anomaly_scores['binarized_scores'] = [1 if x > threshold else 0 for x in anomaly_scores.iloc[:, 0]]

        is_anomaly = original_data['is_anomaly']
        is_anomaly = is_anomaly[1:]

        metrics = performance_metrics(is_anomaly, anomaly_scores['binarized_scores'])

        print(metrics)

        return metrics


    