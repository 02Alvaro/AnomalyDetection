from abc import abstractmethod

from domain.models.BasicReport import BasicReport


class ReportInterface:
    """
    Abstract base class for report saving.

    Methods
    -------
    save(metrics: BasicReport)
        Abstract method for saving the evaluation metrics.
    """

    @abstractmethod
    def save(self, metrics: BasicReport):
        """
        Saves the evaluation metrics.

        Parameters
        ----------
        metrics : BasicReport
            The evaluation metrics to be saved.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in the derived class.
        """
        pass
