import os

import pandas as pd
from application.algorithms.hbos.HbosData import HbosData
from application.services.AlgorithmManager import AlgorithmManager
from application.utils.datapaths import DATA_PATH_DOCKER
from domain.interfaces.AlgorithmExecutor import AlgorithmExecutor
from domain.services.metrics import performance_metrics
from pyod.models.hbos import HBOS
from pyod.utils.utility import standardizer
from sklearn.model_selection import train_test_split


@AlgorithmManager.executor_for(HbosData)
class HbosExecutor(AlgorithmExecutor):
    def execute(self, command: HbosData):
        self.executeAlgorithm(command)

    def executeAlgorithm(self, command: HbosData):
        df = pd.read_csv(os.path.join(DATA_PATH_DOCKER, command.data_file))
        y = df[command.target_variable]
        X = df.drop(command.target_variable, axis=1)
        anomaly_fraction: float = (y == 1).sum() / len(y)

        x_train, x_test, _, y_test = train_test_split(
            X, y, test_size=0.3, random_state=command.random_state
        )
        x_train_norm, x_test_norm = standardizer(x_train, x_test)

        algorithm_instance = HBOS(
            contamination=anomaly_fraction,
            n_bins=command.n_bins,
            alpha=command.alpha,
            tol=command.tol,
        )

        algorithm_instance.fit(x_train_norm)
        y_test_pred = algorithm_instance.predict(x_test_norm)

        metrics = performance_metrics((y_test == 1).astype(int), y_test_pred)
        print(metrics)
