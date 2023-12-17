import os

import pandas as pd
from application.algorithms.lof.LofData import LofData
from application.services.AlgorithmManager import AlgorithmManager
from application.utils.datapaths import DATA_PATH_DOCKER
from domain.interfaces.AlgorithmExecutor import AlgorithmExecutor
from joblib import dump
from pyod.models.lof import LOF
from pyod.utils.utility import standardizer
from sklearn.model_selection import train_test_split


@AlgorithmManager.trainer_for(LofData)
class LofTrainer(AlgorithmExecutor):
    def train(self, command: LofData):
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
        dump(algorithm_instance, command.model_name)
