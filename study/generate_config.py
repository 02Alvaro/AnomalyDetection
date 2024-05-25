import yaml


def generate_config(num_folds=5, num_seeds=1):
    algorithms = ["cblof" ,"hbos","knn","lof"]
    folders = [ "average_activity_type_clicks_avg","average_activity_type_clicks_sum"]
    seeds = [114]  # Example seeds

    config = {
        "algorithms": []
    }

    for algorithm in algorithms:
        for seed in seeds:
            algo_config = {
                "name": algorithm,
                "reportFile": "allReports.csv",
                "train": [],
                "test": []
            }
            for folder in folders:
                for fold in range(1, num_folds + 1):
                    train_data_file = f"{folder}/train_fold_{fold}.csv"
                    test_data_file = f"{folder}/test_fold_{fold}.csv"
                    model_output = f"{algorithm}_model_seed_{seed}_fold_{fold}.pkl"

                    train_config = {
                        "data_file": train_data_file,
                        "model_output": model_output,
                        "parameters": {
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

            config["algorithms"].append(algo_config)

    with open("anomalyDetection/src/config.yaml", "w") as file:
        yaml.dump(config, file, sort_keys=False)

generate_config()
