import os
import json
import pandas as pd
from anomalyDetection.anomalyDetection import performance_metrics

from anomalyDetection.gateway.Algorithms.LstmVae.LstmVaeCommand import LstmVaeCommand
from anomalyDetection.gateway.Interfaces.CommandHandler import CommandHandler
from anomalyDetection.gateway.utils.DockerExecutor import DockerExecutor

class LstmVaeCommandHandler(CommandHandler):


    def execute(self, command: LstmVaeCommand):
        self.dockerAlgorithm(command)
        self.evaluate_performance(command.filePath, 'E:/TFG/anomalyDetection/src/TimeEval-algorithms-main/2-results/anomaly_scoresLstm.ts')

    def dockerAlgorithm(self, command: LstmVaeCommand):
        dockerChain='docker run --rm -v {pwd}/TimeEval-algorithms-main/1-data:/data:ro -v {pwd}/TimeEval-algorithms-main/2-results:/results:rw registry.gitlab.hpi.de/akita/i/lstm_vae:latest execute-algorithm \'{{"executionType": "execute", "dataInput": "/data/{file_name}", "dataOutput": "/results/anomaly_scores.ts", "modelInput": "/results/model.pkl", "modelOutput": "/results/model.pkl", "customParameters": {json_str}}}\''

        pwd = os.getcwd()
        json_str = self.toJson(command)
        docker_command_str = dockerChain.format(pwd=pwd, file_name=command.filePath, json_str=json_str)
        DockerExecutor().execute(docker_command_str)

    def toJson(self, command: LstmVaeCommand):
        custom_params = {
            "learning_rate": command.learning_rate,
            "epochs": command.epochs,
            "batch_size": command.batch_size,
            "window_size": command.window_size,
            "latent_size": command.latent_size,
            "lstm_layers": command.lstm_layers,
            "rnn_hidden_size": command.rnn_hidden_size,
            "early_stopping_delta": command.early_stopping_delta,
            "early_stopping_patience": command.early_stopping_patience,
        }
        
        return json.dumps(custom_params)


    def evaluate_performance(self,original_file, result_file ):
        anomaly_scores = pd.read_csv(result_file)
        original_data = pd.read_csv(original_file)

        threshold = 0.5
        anomaly_scores['binarized_scores'] = [1 if x > threshold else 0 for x in anomaly_scores.iloc[:, 0]]

        is_anomaly = original_data['is_anomaly']
        is_anomaly = is_anomaly[1:]

        metrics = performance_metrics(is_anomaly, anomaly_scores['binarized_scores'])

        return metrics


    