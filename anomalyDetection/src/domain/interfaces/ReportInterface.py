from abc import abstractmethod

from domain.models.BasicReport import BasicReport


class ReportInterface:
    @abstractmethod
    def save(metrics: BasicReport):
        pass
