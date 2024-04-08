import yaml


def generate_config(num_folds=5):
    config = {
        "algorithms": [
            {
                "name": "lof",
                "reportFile": "allReports.csv",
                "train": [],
                "test": []
            }
        ]
    }

    for fold in range(1, num_folds + 1):
        train_config = {
            "data_file": f"fold_excluyendo_parte_{fold}.csv",
            "model_output": f"fold_{fold}.zip",
            "parameters": {
            }
        }
        config["algorithms"][0]["train"].append(train_config)

        test_config = {
            "data_file": f"all_students_click_data_part_{fold}.csv",
            "model_input": f"fold_{fold}.zip"
        }
        config["algorithms"][0]["test"].append(test_config)

    with open("config.yaml", "w") as file:
        yaml.dump(config, file, sort_keys=False)

generate_config(num_folds=5)
