from dataclasses import asdict, fields

import pandas as pd
from application.services.FileSystemService import FileSystemService
from domain.interfaces.AlgorithmData import AlgorithmData
from domain.models.AlgorithmEvaluationMetrics import AlgorithmEvaluationMetrics
from domain.services.metrics import file_info, performance_metrics


class AlgorithmDataProcesor:
    def __init__(self, file_system_service: FileSystemService):
        self.file_system_service = file_system_service

    def process(
        self, algorithm_data: AlgorithmData, prediction_data: pd.DataFrame, time: int
    ) -> AlgorithmEvaluationMetrics:
        try:
            target_variable = algorithm_data.target_variable
            if target_variable is None:
                target_variable = "is_anomaly"
        except AttributeError:
            target_variable = "is_anomaly"

        original_data = self.file_system_service.read_dataFrom(
            algorithm_data.data_file
        )[target_variable]

        # If the original data has more examples than the prediction data, its the header so we remove it
        if original_data.shape[0] > prediction_data.shape[0]:
            original_data = original_data[1:]

        metrics = performance_metrics(
            original_data, prediction_data.round().astype(int)
        )
        metrics["time"] = time

        file_data = self.file_system_service.read_dataFrom(algorithm_data.data_file)
        file_info_results = file_info(file_data)

        param_dict = asdict(algorithm_data)

        base_class_fields = {field.name for field in fields(AlgorithmData)}

        specific_params = {
            key: value
            for key, value in param_dict.items()
            if key not in base_class_fields
        }

        algorithm_evaluation_metrics: AlgorithmEvaluationMetrics = (
            AlgorithmEvaluationMetrics(
                algorithm_name=algorithm_data.__class__.__name__.replace("Data", ""),
                algorithm_parameters=specific_params.__str__().replace(",", ";"),
                dataset_name=algorithm_data.data_file,
                num_examples=file_info_results["num_examples"],
                num_dims=file_info_results["num_dims"],
                anomaly_percentage=file_info_results["anomaly_percentage"],
                metrics=metrics,
            )
        )

        return algorithm_evaluation_metrics
