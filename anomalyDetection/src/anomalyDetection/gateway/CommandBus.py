from anomalyDetection.gateway.Interfaces.Command import Command
from anomalyDetection.gateway.Interfaces.CommandHandler import CommandHandler
from anomalyDetection.gateway.Algorithms.LstmVae.LstmVaeCommandHandler import LstmVaeCommandHandler
from anomalyDetection.gateway.Algorithms.LstmVae.LstmVaeCommand import LstmVaeCommand

class CommandBus:
    def __init__(self):
        self.handlers = {}
        self.register_handler(LstmVaeCommand, LstmVaeCommandHandler())

    def register_handler(self, command_type, handler: CommandHandler):
        self.handlers[command_type] = handler

    def execute(self, command: Command):
        handler = self.handlers.get(type(command))
        if handler is None:
            raise Exception(f"No handler found for command type {type(command).__name__}")
        handler.execute(command)
