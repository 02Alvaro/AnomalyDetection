import yaml


def generate_config(num_folds=5, num_seeds=10):
    algorithms = ["cblof" ,"hbos","knn","lof","autoencoder","dae"]
    folders = [ "activity_type_clicks_sum"]
    code_modules = ['AAA', 'BBB', 'CCC', 'DDD', 'EEE', 'FFF', 'GGG']
    seeds = [114,99,25,76,9,160,53,60,30,170] 

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
                for code_module in code_modules:
                    for fold in range(1, num_folds + 1):
                        train_data_file = f"{folder}/{code_module}/train_fold_{fold}.csv"
                        train_no_anomaly_data_file = f"{folder}/{code_module}/train_no_anomaly_fold_{fold}.csv"
                        test_data_file = f"{folder}/{code_module}/test_fold_{fold}.csv"
                        model_output = f"{algorithm}_{folder}_{code_module}_fold_{fold}_seed_{seed}.pkl"

                        if algorithm in [ "autoencoder","dae"]:
                            train_data_file = train_no_anomaly_data_file

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
