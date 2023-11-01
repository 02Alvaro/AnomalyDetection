import os
from time import time

import numpy as np
import pandas as pd
import yaml
from anomalyDetection.gateway.Algorithms.AlgorithmCommandFactory import (
    AlgorithmCommandFactory,
)
from anomalyDetection.gateway.Interfaces.CommandBus import CommandBus
from anomalyDetection.gateway.utils.CommandFactory import CommandFactory
from joblib import Parallel, delayed

from anomalyDetection.anomalyDetection import process_dataset, randomize


def main():
    csv_datasets = ["AAA.csv"]
    classifiers_parameters = {
        "COF": randomize(),
        "KNN": randomize(),
        "CBLOF": randomize(),
        "HBOS": randomize(),
        "LOF": randomize(),
    }
    random_state = np.random.RandomState(42)
    target_variable = "final_result"

    dataset_results = Parallel(n_jobs=-1)(
        delayed(process_dataset)(
            csv_dataset, classifiers_parameters, random_state, target_variable
        )
        for csv_dataset in csv_datasets
    )

    all_results_data = []
    for (
        dataset_name,
        num_examples,
        num_dims,
        anomaly_percentage,
        all_clf_metrics,
    ) in dataset_results:
        for clf_metrics in all_clf_metrics:
            clf_name = clf_metrics["clf"]
            param_value = classifiers_parameters.get(clf_name)
            result_dict = {
                "Algoritmo": clf_name,
                "Parámetro": param_value,
                "Datos": dataset_name,
                "#Ejemplos": num_examples,
                "#Dimensiones": num_dims,
                "Anomalías(%)": anomaly_percentage,
                "t": clf_metrics["time"],
                "se": clf_metrics["se"],
                "sp": clf_metrics["sp"],
                "p": clf_metrics["p"],
                "roc": clf_metrics["roc"],
            }
            all_results_data.append(result_dict)

        all_results_df = pd.DataFrame(all_results_data).sort_values(
            by="roc", ascending=False
        )

        all_results_df.to_csv(
            os.path.join(os.getcwd(), "metrics", "all_results.csv"), index=False
        )


def main3():
    commandBus = CommandBus()
    commandBus.execute(
        AlgorithmCommandFactory.create_command("lstm_vae", "Processed_AAA.csv")
    )


class ConfigLoader:
    @staticmethod
    def load_config(config_path="/app/src/config.yaml"):
        with open(config_path, "r") as file:
            return yaml.safe_load(file)


def main4():
    config = ConfigLoader.load_config()
    commands = CommandFactory.create_commands_from_config(config)

    commandBus = CommandBus()
    for command in commands:
        commandBus.execute(command)


def main5():
    print(os.path.abspath(__file__))


if __name__ == "__main__":
    t0 = time()
    main4()
    t1 = time()
    print(f"Tiempo total: {round(t1 - t0, ndigits=4)} segundos")
