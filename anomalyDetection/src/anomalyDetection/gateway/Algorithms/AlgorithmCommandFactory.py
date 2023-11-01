from anomalyDetection.gateway.Algorithms.dae.DaeCommand import DaeCommand
from anomalyDetection.gateway.Algorithms.LstmVae.LstmVaeCommand import LstmVaeCommand


class AlgorithmCommandFactory:
    @staticmethod
    def create_command(algorithm_name, file_name, **kwargs):
        if algorithm_name == "lstm_vae":
            return LstmVaeCommand(filePath=file_name, **kwargs)
        elif algorithm_name == "dae":
            return DaeCommand(filePath=file_name, **kwargs)
