import os
from random import randint
from time import time

import pandas as pd
from application.algorithms.lof.LofConfiguration import LofConfiguration
from application.services.AlgorithmDataProcesor import AlgorithmDataProcesor
from application.services.AlgorithmManager import AlgorithmManager
from application.services.FileSystemService import FileSystemService
from application.services.PyodWrapper import PyodWrapper
from domain.interfaces.AlgorithmEvaluate import AlgorithmEvaluate
from domain.interfaces.ReportInterface import ReportInterface
from domain.models.BasicReport import BasicReport
from inject import Inject
from pyod.models.lof import LOF as LOF


@AlgorithmManager.evaluator_for(LofConfiguration)
@Inject
class Lof(AlgorithmEvaluate):
    """
    Class for evaluating an LOF algorithm configuration.

    Attributes
    ----------
    algorithm_data_procesor : AlgorithmDataProcesor
        Service to process algorithm data.
    pyod_service : PyodWrapper
        Wrapper for the PyOD library.
    repository : ReportInterface
        Interface for report storage.
    file_system_service : FileSystemService
        Service for file system operations.
    """

    def __init__(
        self,
        algorithm_data_procesor: AlgorithmDataProcesor,
        pyod_service: PyodWrapper,
        repository: ReportInterface,
        file_system_service: FileSystemService,
    ):
        """
        Initializes the LOF evaluator with the provided services.

        Parameters
        ----------
        algorithm_data_procesor : AlgorithmDataProcesor
            Service to process algorithm data.
        pyod_service : PyodWrapper
            Wrapper for the PyOD library.
        repository : ReportInterface
            Interface for report storage.
        file_system_service : FileSystemService
            Service for file system operations.
        """
        self.pyod_service = pyod_service
        self.algorithm_data_procesor = algorithm_data_procesor
        self.repository = repository
        self.file_system_service = file_system_service

    def evaluate(self, data: LofConfiguration):
        """
        Evaluates the LOF configuration with the provided data.

        Parameters
        ----------
        data : LofConfiguration
            Configuration data for the LOF algorithm.

        Returns
        -------
        None
        """
        output_file_name = data.__class__.__name__.replace("Configuration", "")
        output_file_name = f"{output_file_name}_{randint(1000, 9999)}_{os.path.basename(data.data_file)}"

        fileData = self.file_system_service.read_dataFrom(data.data_file)

        if "is_anomaly" in fileData.columns:
            fileData = fileData.drop(columns=["is_anomaly"])

        algorithm_instance: LOF = self.pyod_service.loadModel(data.model_name)

        t0 = time()
        predictedData = algorithm_instance.predict(fileData)
        t1 = time()

        executionTime = round(t1 - t0, ndigits=4)

        processed_data = pd.DataFrame(predictedData)
        self.file_system_service.save_resultsTo(output_file_name, processed_data)

        algorithm_evaluation_metrics: BasicReport = (
            self.algorithm_data_procesor.process(data, processed_data, executionTime)
        )
        self.repository.save(algorithm_evaluation_metrics, data.report_file)
