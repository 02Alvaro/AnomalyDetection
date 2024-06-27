import copy

import yaml


def generate_param_config(num_folds=5, num_seeds=10):
    algorithms = {
        "knn": "n_neighbors",
        "lof": "n_neighbors",
        "cof": "n_neighbors",
        "cblof": "n_clusters",
        "hbos": "n_bins",
        "autoencoder": "latent_size",
        "dae": "latent_size",
    }
    folders = ["activity_type_clicks_sum"]
    code_modules = ['AAA', 'BBB', 'CCC', 'DDD', 'EEE', 'FFF', 'GGG']
    seeds = [114, 99, 25, 76, 9, 160, 53, 60, 30, 170]

    param_values = {
        "n_neighbors": [5, 10, 20, 30, 40],
        "n_clusters": [6,7,8,9,10],
        "n_bins": [5, 10, 15, 20, 25],
        "latent_size": [16, 32, 64, 128, 256]
    }

    config = {
        "algorithms": []
    }

    for algorithm, param in algorithms.items():
        algo_config = {
            "name": algorithm,
            "reportFile": f"{algorithm}allReports.csv",
            "train": [],
            "test": []
        }
        for seed in seeds:
            for folder in folders:
                for code_module in code_modules:
                    for fold in range(1, num_folds + 1):
                        for value in param_values[param]:
                            train_data_file = f"{folder}/{code_module}/train_fold_{fold}.csv"
                            test_data_file = f"{folder}/{code_module}/test_fold_{fold}.csv"
                            model_output = f"{algorithm}_{folder}_{code_module}_fold_{fold}_seed_{seed}_{value}.pkl"

                            if algorithm == "dae" or algorithm == "autoencoder":
                                train_data_file = f"{folder}/{code_module}/train_no_anomaly_fold_{fold}.csv"

                            train_config = {
                                "data_file": train_data_file,
                                "model_output": model_output,
                                "parameters": {
                                    param: value,
                                    "seed": seed
                                }
                            }
                            test_config = {
                                "data_file": train_data_file,
                                "model_input": model_output
                            }
                            test_config_alt = {
                                "data_file": test_data_file,
                                "model_input": model_output
                            }

                            algo_config["train"].append(train_config)
                            algo_config["test"].append(test_config)
                            algo_config["test"].append(test_config_alt)

        config["algorithms"].append(copy.deepcopy(algo_config))


    with open("anomalyDetection/src/config.yaml", "w") as file:
        yaml.dump(config, file, sort_keys=False)

generate_param_config()
