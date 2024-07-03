from dataclasses import asdict, fields

from application.algorithms.autoencoder.AutoEncoderConfiguration import \
    AutoEncoderConfiguration
from application.services.AlgorithmManager import AlgorithmManager
from application.services.TimeEvalWrapper import (TimeEvalParameters,
                                                  TimeEvalWrapper)
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator
from domain.interfaces.AlgorithmTrainer import AlgorithmTrainer
from domain.interfaces.TrainRepository import TrainRepository
from inject import Inject


@AlgorithmManager.trainer_for(AutoEncoderConfiguration)
@Inject
class AutoEncoderTrainer(AlgorithmTrainer):
    """
    Trainer class for the AutoEncoder algorithm.

    Attributes:
        time_eval_wrapper (TimeEvalWrapper): Wrapper for time evaluation.
        repository (TrainRepository): Repository for storing training data.
    """

    def __init__(
        self,
        time_eval_wrapper: TimeEvalWrapper,
        repository: TrainRepository,
    ):
        """
        Initializes the AutoEncoder trainer with the provided services.

        Args:
            time_eval_wrapper (TimeEvalWrapper): Wrapper for time evaluation.
            repository (TrainRepository): Repository for storing training data.
        """
        self.time_eval_wrapper = time_eval_wrapper
        self.repository = repository

    def train(self, data: AutoEncoderConfiguration):
        """
        Trains the AutoEncoder with the given configuration.

        Args:
            data (AutoEncoderConfiguration): Configuration data for the AutoEncoder.

        Returns:
            None
        """
        param_dict = asdict(data)

        base_class_fields = {field.name for field in fields(AlgorithmConfigurator)}

        specific_params = {
            key: value
            for key, value in param_dict.items()
            if key not in base_class_fields
        }

        specific_params["random_state"] = data.seed

        time_eval_parameters = TimeEvalParameters(
            name="autoencoder",
            execution_type="train",
            data_input=data.data_file,
            model_output=data.model_name,
            parameters=specific_params,
        )

        self.time_eval_wrapper.execute(time_eval_parameters)

        base_class_fields = {field.name for field in fields(AlgorithmConfigurator)}

        specific_params = specific_params.__str__().replace(",", ";")

        self.repository.save(data)
