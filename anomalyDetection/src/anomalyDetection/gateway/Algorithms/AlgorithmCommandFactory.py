from anomalyDetection.gateway.Algorithms.LstmVae.LstmVaeCommand import LstmVaeCommand

class AlgorithmCommandFactory:
    @staticmethod
    def create_command(algorithm_name, file_name):
        if algorithm_name == 'lstm_vae':
            return LstmVaeCommand(filePath=file_name)
