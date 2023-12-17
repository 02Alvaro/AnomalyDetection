import os

import pandas as pd
from application.algorithms.lof.LofData import LofData
from application.services.AlgorithmManager import AlgorithmManager
from application.utils.datapaths import DATA_PATH_DOCKER
from domain.interfaces.AlgorithmExecutor import AlgorithmExecutor
from domain.services.AlgorithmDataProcesor import AlgorithmDataProcesor
from domain.services.metrics import performance_metrics
from inject import Inject
from pyod.models.lof import LOF
from pyod.utils.utility import standardizer
from sklearn.model_selection import train_test_split


@AlgorithmManager.executor_for(LofData)
class LofExecutor(AlgorithmExecutor):
    @Inject
    def __init__(self, data_procesor: AlgorithmDataProcesor):
        self.data_procesor = data_procesor

    def execute(self, command: LofData):
        self.executeAlgorithm(command)

    def executeAlgorithm(self, command: LofData):
        df = pd.read_csv(os.path.join(DATA_PATH_DOCKER, command.data_file))
        y = df[command.target_variable]
        X = df.drop(command.target_variable, axis=1)
        anomaly_fraction: float = (y == 1).sum() / len(y)

        x_train, x_test, _, y_test = train_test_split(
            X, y, test_size=0.3, random_state=command.random_state
        )
        x_train_norm, x_test_norm = standardizer(x_train, x_test)

        algorithm_instance = LOF(
            n_neighbors=command.n_neighbors,
            algorithm=command.algorithm,
            leaf_size=command.leaf_size,
            metric=command.metric,
            p=command.p,
            metric_params=command.metric_params,
            contamination=command.contamination,
            n_jobs=command.n_jobs,
            novelty=command.novelty,
        )

        algorithm_instance.fit(x_train_norm)
        y_test_pred = algorithm_instance.predict(x_test_norm)
        print(y_test)
        metrics = performance_metrics(y_test, y_test_pred)
        print(metrics)
