import os

import pandas as pd
from application.algorithms.cof.CofData import CofData
from application.services.AlgorithmManager import AlgorithmManager
from application.utils.datapaths import DATA_PATH_DOCKER, RESULTS_PATH_DOCKER
from domain.interfaces.AlgorithmExecutor import AlgorithmExecutor
from domain.services.metrics import performance_metrics
from pyod.models.cof import COF
from pyod.utils.utility import standardizer
from sklearn.model_selection import train_test_split


@AlgorithmManager.executor_for(CofData)
class CofExecutor(AlgorithmExecutor):
    def execute(self, command: CofData):
        self.executeAlgorithm(command)

    def executeAlgorithm(self, command: CofData):
        df = pd.read_csv(os.path.join(DATA_PATH_DOCKER, command.file_path))
        y = df[command.tarjet_variable]
        X = df.drop(command.tarjet_variable, axis=1)
        anomaly_fraction: float = (y == 1).sum() / len(y)

        x_train, x_test, _, y_test = train_test_split(
            X, y, test_size=0.3, random_state=command.random_state
        )
        x_train_norm, x_test_norm = standardizer(x_train, x_test)

        algorithm_instance = COF(
            contamination=anomaly_fraction,
            n_neighbors=command.n_neighbors,
            method=command.method,
        )

        algorithm_instance.fit(x_train_norm)
        y_test_pred = algorithm_instance.predict(x_test_norm)

        metrics = performance_metrics((y_test == 1).astype(int), y_test_pred)
        print(metrics)
