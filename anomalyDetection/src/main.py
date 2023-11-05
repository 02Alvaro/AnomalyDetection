from time import time

from application.factories.FileAlgorithmFactory import FileAlgorithmFactory
from application.services.AlgorithmManager import AlgorithmManager

"""
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
"""

import application.algorithms


def main():
    commands = FileAlgorithmFactory.create_from_config()
    for command in commands:
        AlgorithmManager.execute(command)


if __name__ == "__main__":
    t0 = time()
    main()
    t1 = time()
    print(f"Tiempo total: {round(t1 - t0, ndigits=4)} segundos")
