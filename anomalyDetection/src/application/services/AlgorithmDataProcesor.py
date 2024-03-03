from dataclasses import asdict, fields

import pandas as pd
from application.services.FileSystemService import FileSystemService
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator
from domain.models.BasicReport import BasicReport
from domain.services.metrics import file_info, performance_metrics


class AlgorithmDataProcesor:
    def __init__(self, file_system_service: FileSystemService):
        self.file_system_service = file_system_service

    def process(
        self,
        algorithm_data: AlgorithmConfigurator,
        prediction_data: pd.DataFrame,
        time: int,
    ) -> BasicReport:
        try:
            target_variable = algorithm_data.target_variable
            if target_variable is None:
                target_variable = "is_anomaly"
        except AttributeError:
            target_variable = "is_anomaly"

        print(f"Target variable: {target_variable}")
        print(f"Algorithm data: {algorithm_data}")
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

        algorithm_evaluation_metrics: BasicReport = BasicReport(
            algorithm_name=algorithm_data.__class__.__name__.replace(
                "Configuration", ""
            ),
            model=algorithm_data.model_name,
            dataset_name=algorithm_data.data_file,
            num_examples=file_info_results["num_examples"],
            num_dims=file_info_results["num_dims"],
            anomaly_percentage=file_info_results["anomaly_percentage"],
            metrics=metrics,
        )

        return algorithm_evaluation_metrics
