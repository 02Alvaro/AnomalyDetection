import os
from random import randint
from time import time

import pandas as pd
from application.algorithms.lstmVae.LstmVaeData import LstmVaeData
from application.services.AlgorithmManager import AlgorithmManager
from application.services.TimeEvalWrapper import TimeEvalParameters, TimeEvalWrapper
from application.utils.datapaths import RESULTS_PATH_DOCKER
from domain.interfaces.AlgorithmExecutor import AlgorithmExecutor
from domain.interfaces.EvaluationRepository import EvaluationRepository
from domain.models.AlgorithmEvaluationMetrics import AlgorithmEvaluationMetrics
from domain.services.AlgorithmDataProcesor import AlgorithmDataProcesor
from inject import Inject


@AlgorithmManager.executor_for(LstmVaeData)
@Inject
class LstmVaeExecutor(AlgorithmExecutor):
    def __init__(
        self,
        algorithm_data_procesor: AlgorithmDataProcesor,
        time_eval_wrapper: TimeEvalWrapper,
        repository: EvaluationRepository,
    ):
        self.time_eval_wrapper = time_eval_wrapper
        self.algorithm_data_procesor = algorithm_data_procesor
        self.repository = repository

    def execute(self, data: LstmVaeData):
        output_file_name = (
            f"{data.__class__.__name__}_{randint(1000,9999)}_{data.data_file}"
        )

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

        processed_data = pd.read_csv(
            os.path.join(RESULTS_PATH_DOCKER, output_file_name)
        )

        algorithm_evaluation_metrics: AlgorithmEvaluationMetrics = (
            self.algorithm_data_procesor.process(data, processed_data, executionTime)
        )

        self.repository.save(algorithm_evaluation_metrics)
