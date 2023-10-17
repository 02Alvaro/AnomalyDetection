''''
import os
import json
import pandas as pd

from anomalyDetection.src.anomalyDetection.gateway.utils.DockerExecutor import DockerExecutor
from .DockerCommand import DockerCommand
from ..anomalyDetection import performance_metrics

class CommandHandler:

    def __init__(self):
        self.algorithm_map = {
            'lstm_vae': 'docker run --rm -v {pwd}/TimeEval-algorithms-main/1-data:/data:ro -v {pwd}/TimeEval-algorithms-main/2-results:/results:rw registry.gitlab.hpi.de/akita/i/lstm_vae:latest execute-algorithm \'{{"executionType": "train", "dataInput": "/data/{file_name}", "dataOutput": "/results/anomaly_scores.ts", "modelInput": "/results/model.pkl", "modelOutput": "/results/model.pkl", "customParameters": {{json_str}}}}\''
        }

    def run_algorithm(self, algorithm_name, file_name, json_args):
        pwd = os.getcwd()
        json_str = json.dumps(json_args)
        docker_command_str = self.algorithm_map.get(algorithm_name).format(pwd=pwd, file_name=file_name, json_str=json_str)
        DockerExecutor.execute(docker_command_str)
        
        return self.evaluate_performance('E:/TFG/anomalyDetection/src/TimeEval-algorithms-main/2-results/anomaly_scores.ts', 'E:/TFG/anomalyDetection/src/TimeEval-algorithms-main/1-data/dataset.csv')

    def evaluate_performance(self, result_file, original_file):
        anomaly_scores = pd.read_csv(result_file)
        original_data = pd.read_csv(original_file)

        threshold = 0.5
        anomaly_scores['binarized_scores'] = [1 if x > threshold else 0 for x in anomaly_scores.iloc[:, 0]]

            
        is_anomaly = original_data['is_anomaly']
        is_anomaly = is_anomaly[1:]

        metrics = performance_metrics(is_anomaly, anomaly_scores['binarized_scores'])

        return metrics

'''