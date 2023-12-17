import os
from dataclasses import asdict, fields
from random import randint

import pandas as pd
from application.algorithms.lstmVae.LstmVaeData import LstmVaeData
from application.services.AlgorithmManager import AlgorithmManager
from application.services.TimeEvalWrapper import TimeEvalParameters, TimeEvalWrapper
from domain.interfaces.AlgorithmData import AlgorithmData
from domain.interfaces.AlgorithmTrainer import AlgorithmTrainer
from inject import Inject


@AlgorithmManager.trainer_for(LstmVaeData)
@Inject
class LstmVaeTrainer(AlgorithmTrainer):
    def __init__(
        self,
        time_eval_wrapper: TimeEvalWrapper,
    ):
        self.time_eval_wrapper = time_eval_wrapper

    def train(self, data: LstmVaeData):
        param_dict = asdict(data)

        base_class_fields = {field.name for field in fields(AlgorithmData)}

        specific_params = {
            key: value
            for key, value in param_dict.items()
            if key not in base_class_fields
        }

        time_eval_parameters = TimeEvalParameters(
            name="lstm_vae",
            execution_type="train",
            data_input=data.data_file,
            model_output=data.model_name,
            parameters=specific_params,
        )

        self.time_eval_wrapper.execute(time_eval_parameters)
