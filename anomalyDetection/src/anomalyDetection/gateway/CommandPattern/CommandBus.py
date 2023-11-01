from anomalyDetection.gateway.Algorithms.autoencoder.AutoEncoderCommand import (
    AutoEncoderCommand,
)
from anomalyDetection.gateway.Algorithms.autoencoder.AutoEncoderCommandHandler import (
    AutoEncoderCommandHandler,
)
from anomalyDetection.gateway.Algorithms.dae.DaeCommand import DaeCommand
from anomalyDetection.gateway.Algorithms.dae.DaeCommandHandler import DaeCommandHandler
from anomalyDetection.gateway.Algorithms.LstmVae.LstmVaeCommand import LstmVaeCommand
from anomalyDetection.gateway.Algorithms.LstmVae.LstmVaeCommandHandler import (
    LstmVaeCommandHandler,
)
from anomalyDetection.gateway.CommandPattern.Command import Command
from anomalyDetection.gateway.CommandPattern.CommandHandler import CommandHandler


class CommandBus:
    def __init__(self):
        self.handlers = {}
        self.register_handler(LstmVaeCommand, LstmVaeCommandHandler())
        self.register_handler(DaeCommand, DaeCommandHandler())
        self.register_handler(AutoEncoderCommand, AutoEncoderCommandHandler())

    def register_handler(self, command_type, handler: CommandHandler):
        self.handlers[command_type] = handler

    def execute(self, command: Command):
        handler = self.handlers.get(type(command))
        if handler is None:
            raise Exception(
                f"No handler found for command type {type(command).__name__}"
            )
        handler.execute(command)
