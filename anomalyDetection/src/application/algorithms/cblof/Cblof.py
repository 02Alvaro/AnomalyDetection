import os
from random import randint
from time import time

import pandas as pd
from application.algorithms.cblof.CblofConfiguration import CblofConfiguration
from application.services.AlgorithmDataProcesor import AlgorithmDataProcesor
from application.services.AlgorithmManager import AlgorithmManager
from application.services.FileSystemService import FileSystemService
from application.services.PyodWrapper import PyodWrapper
from domain.interfaces.AlgorithmEvaluate import AlgorithmEvaluate
from domain.interfaces.ReportInterface import ReportInterface
from domain.models.BasicReport import BasicReport
from inject import Inject
from pyod.models.cblof import CBLOF


@AlgorithmManager.evaluator_for(CblofConfiguration)
@Inject
class Cblof(AlgorithmEvaluate):
    def __init__(
        self,
        algorithm_data_procesor: AlgorithmDataProcesor,
        pyod_service: PyodWrapper,
        repository: ReportInterface,
        file_system_service: FileSystemService,
    ):
        self.pyod_service = pyod_service
        self.algorithm_data_procesor = algorithm_data_procesor
        self.repository = repository
        self.file_system_service = file_system_service

    def evaluate(self, data: CblofConfiguration):
        output_file_name = data.__class__.__name__.replace("Configuration", "")
        output_file_name = f"{output_file_name}_{randint(1000,9999)}_{os.path.basename(data.data_file)}"

        fileData = self.file_system_service.read_dataFrom(data.data_file)

        algorithm_instance: CBLOF = self.pyod_service.loadModel(data.model_name)

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
