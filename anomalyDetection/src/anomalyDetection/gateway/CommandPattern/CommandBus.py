from anomalyDetection.gateway.CommandPattern.Command import Command, CommandHandler


class CommandBus:
    def __init__(self):
        self.handlers = {}

    def register(self, command_type, handler: CommandHandler):
        self.handlers[command_type] = handler

    def execute(self, command: Command):
        handler = self.handlers.get(type(command))
        if handler is None:
            raise Exception(f"No handler found for {type(command).__name__}")
        handler.execute(command)
