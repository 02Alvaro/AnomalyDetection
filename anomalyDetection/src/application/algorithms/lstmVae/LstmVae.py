import os
from random import randint
from time import time

from application.algorithms.lstmVae.LstmVaeConfiguration import \
    LstmVaeConfiguration
from application.services.AlgorithmDataProcesor import AlgorithmDataProcesor
from application.services.AlgorithmManager import AlgorithmManager
from application.services.FileSystemService import FileSystemService
from application.services.TimeEvalWrapper import (TimeEvalParameters,
                                                  TimeEvalWrapper)
from domain.interfaces.AlgorithmEvaluate import AlgorithmEvaluate
from domain.interfaces.ReportInterface import ReportInterface
from domain.models.BasicReport import BasicReport
from inject import Inject


@AlgorithmManager.evaluator_for(LstmVaeConfiguration)
@Inject
class LstmVae(AlgorithmEvaluate):
    """
    Class for evaluating an LSTM-VAE algorithm configuration.

    Attributes
    ----------
    algorithm_data_procesor : AlgorithmDataProcesor
        Service to process algorithm data.
    time_eval_wrapper : TimeEvalWrapper
        Wrapper for time evaluation.
    repository : ReportInterface
        Interface for report storage.
    file_system_service : FileSystemService
        Service for file system operations.
    """

    def __init__(
        self,
        algorithm_data_procesor: AlgorithmDataProcesor,
        time_eval_wrapper: TimeEvalWrapper,
        repository: ReportInterface,
        file_system_service: FileSystemService,
    ):
        """
        Initializes the LSTM-VAE evaluator with the provided services.

        Parameters
        ----------
        algorithm_data_procesor : AlgorithmDataProcesor
            Service to process algorithm data.
        time_eval_wrapper : TimeEvalWrapper
            Wrapper for time evaluation.
        repository : ReportInterface
            Interface for report storage.
        file_system_service : FileSystemService
            Service for file system operations.
        """
        self.time_eval_wrapper = time_eval_wrapper
        self.algorithm_data_procesor = algorithm_data_procesor
        self.repository = repository
        self.file_system_service = file_system_service

    def evaluate(self, data: LstmVaeConfiguration):
        """
        Evaluates the LSTM-VAE configuration with the provided data.

        Parameters
        ----------
        data : LstmVaeConfiguration
            Configuration data for the LSTM-VAE algorithm.

        Returns
        -------
        None
        """
        output_file_name = data.__class__.__name__.replace("Configuration", "")
        output_file_name = f"{output_file_name}_{randint(1000, 9999)}_{os.path.basename(data.data_file)}"

        time_eval_parameters = TimeEvalParameters(
            name="lstm_vae",
            execution_type="execute",
            model_input=data.model_name,
            data_input=data.data_file,
            data_output=output_file_name,
        )

        t0 = time()
        self.time_eval_wrapper.execute(time_eval_parameters)
        t1 = time()

        executionTime = round(t1 - t0, ndigits=4)

        processed_data = self.file_system_service.read_resultsFrom(output_file_name)

        algorithm_evaluation_metrics: BasicReport = (
            self.algorithm_data_procesor.process(data, processed_data, executionTime)
        )
        self.repository.save(algorithm_evaluation_metrics, data.report_file)
