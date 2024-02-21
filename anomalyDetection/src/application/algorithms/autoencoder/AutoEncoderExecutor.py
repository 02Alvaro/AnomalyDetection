import os
from dataclasses import asdict
from random import randint
from time import time

from application.algorithms.autoencoder.AutoEncoderData import AutoEncoderData
from application.services.AlgorithmDataProcesor import AlgorithmDataProcesor
from application.services.AlgorithmManager import AlgorithmManager
from application.services.FileSystemService import FileSystemService
from application.services.TimeEvalWrapper import TimeEvalParameters, TimeEvalWrapper
from domain.interfaces.AlgorithmExecutor import AlgorithmExecutor
from domain.interfaces.EvaluationRepository import EvaluationRepository
from domain.models.AlgorithmEvaluationMetrics import AlgorithmEvaluationMetrics
from inject import Inject


@AlgorithmManager.executor_for(AutoEncoderData)
@Inject
class AutoEncoderExecutor(AlgorithmExecutor):
    def __init__(
        self,
        algorithm_data_procesor: AlgorithmDataProcesor,
        time_eval_wrapper: TimeEvalWrapper,
        repository: EvaluationRepository,
        file_system_service: FileSystemService,
    ):
        self.time_eval_wrapper = time_eval_wrapper
        self.algorithm_data_procesor = algorithm_data_procesor
        self.repository = repository
        self.file_system_service = file_system_service

    def execute(self, data: AutoEncoderData):
        output_file_name = data.__class__.__name__.replace("Data", "")
        output_file_name = f"{output_file_name}_{randint(1000,9999)}_{os.path.basename(data.data_file)}"

        time_eval_parameters = TimeEvalParameters(
            name="autoencoder",
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

        algorithm_evaluation_metrics: AlgorithmEvaluationMetrics = (
            self.algorithm_data_procesor.process(data, processed_data, executionTime)
        )
        self.repository.save(algorithm_evaluation_metrics, data.report_file)
