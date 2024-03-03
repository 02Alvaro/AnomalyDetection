import yaml
from application.factories.AlgorithmFactory import AlgorithmFactory


class ConfigLoader:
    def __init__(self, config_path):
        self.config_path = config_path

    def load_config(self):
        with open(self.config_path, "r") as file:
            return yaml.safe_load(file)


class AlgorithmFileConfigurationFactory:
    def __init__(self, config: ConfigLoader):
        self.configLoader = config

    def create_from_config(self):
        config = self.configLoader.load_config()
        actions = {"trains": [], "tests": [], "train_test": []}

        for algorithm_config in config.get("algorithms", []):
            algorithm_name = algorithm_config["name"]
            reportFile = algorithm_config.get("reportFile", "report.csv")

            for train in algorithm_config.get("train", []):
                data_file = train["data_file"]
                model_output = train.get("model_output", "")
                parameters = train["parameters"]
                train_executer = AlgorithmFactory.create(
                    algorithm_name,
                    data_file,
                    model_name=model_output,
                    report_file=reportFile,
                    **parameters
                )
                actions["trains"].append(train_executer)

            for train_test in algorithm_config.get("train_test", []):
                data_file_train = train_test["data_file_train"]
                data_file_test = train_test["data_file_test"]
                model_output = train_test.get("model_output")
                parameters = train_test["parameters"]

                train_executer = AlgorithmFactory.create(
                    algorithm_name,
                    data_file_train,
                    model_name=model_output,
                    report_file=reportFile,
                    **parameters
                )
                actions["trains"].append(train_executer)

                test_executer = AlgorithmFactory.create(
                    algorithm_name,
                    data_file_test,
                    model_name=model_output,
                    report_file=reportFile,
                )
                actions["tests"].append(test_executer)

            for test in algorithm_config.get("test", []):
                data_file = test["data_file"]
                model_input = test.get("model_input", "")
                test_executer = AlgorithmFactory.create(
                    algorithm_name,
                    data_file,
                    model_name=model_input,
                    report_file=reportFile,
                )
                actions["tests"].append(test_executer)

        return actions
