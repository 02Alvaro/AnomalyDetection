from abc import ABC, abstractmethod
from anomalyDetection.gateway.Interfaces.Command import Command

class CommandHandler(ABC):
    @abstractmethod
    def execute(self,command:Command):
        pass
