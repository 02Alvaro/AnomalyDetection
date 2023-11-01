from anomalyDetection.gateway.Algorithms.LstmVae.LstmVaeCommand import LstmVaeCommand
from anomalyDetection.gateway.Algorithms.LstmVae.LstmVaeCommandHandler import (
    LstmVaeCommandHandler,
)
from anomalyDetection.gateway.CommandPattern.Command import Command
from anomalyDetection.gateway.CommandPattern.CommandBus import CommandBus
from anomalyDetection.gateway.CommandPattern.CommandHandler import CommandHandler


class AlgorithmBus(CommandBus):
    def __init__(self):
        super().__init__()
