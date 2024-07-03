import yaml
from application.factories.AlgorithmFactory import AlgorithmFactory


class ConfigLoader:
    """
    Class for loading configuration files.

    Attributes
    ----------
    config_path : str
        Path to the configuration file.
    """

    def __init__(self, config_path):
        """
        Initializes the ConfigLoader with the given configuration file path.

        Parameters
        ----------
        config_path : str
            Path to the configuration file.
        """
        self.config_path = config_path

    def load_config(self):
        """
        Loads the configuration from the file.

        Returns
        -------
        dict
            The configuration loaded from the file.
        """
        with open(self.config_path, "r") as file:
            return yaml.safe_load(file)


class AlgorithmFileConfigurationFactory:
    """
    Factory class for creating algorithm configurations from a file.

    Attributes
    ----------
    configLoader : ConfigLoader
        Instance of ConfigLoader to load the configuration file.
    """

    def __init__(self, config: ConfigLoader):
        """
        Initializes the AlgorithmFileConfigurationFactory with the given ConfigLoader.

        Parameters
        ----------
        config : ConfigLoader
            Instance of ConfigLoader to load the configuration file.
        """
        self.configLoader = config

    def create_from_config(self):
        """
        Creates algorithm configurations from the loaded configuration file.

        Returns
        -------
        dict
            A dictionary containing lists of train and test executers.
        """
        config = self.configLoader.load_config()
        actions = {"trains": [], "tests": []}

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

            for train_test in algorithm_config.get("train-test", []):
                data_file_train = train_test["data_file_train"]
                data_file_test = train_test["data_file_test"]
                model = train_test["model"]
                parameters = train_test["parameters"]

                train_executer = AlgorithmFactory.create(
                    algorithm_name,
                    data_file=data_file_train,
                    model_name=model,
                    report_file=reportFile,
                    **parameters
                )
                actions["trains"].append(train_executer)

                test_executer = AlgorithmFactory.create(
                    algorithm_name,
                    data_file=data_file_test,
                    model_name=model,
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
