from abc import ABC, abstractmethod

from anomalyDetection.gateway.CommandPattern.Command import Command


class CommandHandler(ABC):
    @abstractmethod
    def execute(self, command: Command):
        pass
