from dataclasses import asdict, fields

from application.algorithms.dae.DaeConfiguration import DaeConfiguration
from application.services.AlgorithmManager import AlgorithmManager
from application.services.TimeEvalWrapper import TimeEvalParameters, TimeEvalWrapper
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator
from domain.interfaces.AlgorithmTrainer import AlgorithmTrainer
from domain.interfaces.TrainRepository import TrainRepository
from inject import Inject


@AlgorithmManager.trainer_for(DaeConfiguration)
@Inject
class DaeTrainer(AlgorithmTrainer):
    def __init__(
        self,
        time_eval_wrapper: TimeEvalWrapper,
        repository: TrainRepository,
    ):
        self.time_eval_wrapper = time_eval_wrapper
        self.repository = repository

    def train(self, data: DaeConfiguration):
        param_dict = asdict(data)

        base_class_fields = {field.name for field in fields(AlgorithmConfigurator)}

        specific_params = {
            key: value
            for key, value in param_dict.items()
            if key not in base_class_fields
        }

        time_eval_parameters = TimeEvalParameters(
            name="dae",
            execution_type="train",
            data_input=data.data_file,
            model_output=data.model_name,
            parameters=specific_params,
        )

        self.time_eval_wrapper.execute(time_eval_parameters)

        self.repository.save(data)
