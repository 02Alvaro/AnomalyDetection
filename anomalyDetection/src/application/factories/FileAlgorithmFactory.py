import yaml
from application.factories.AlgorithmDataFactory import AlgorithmDataFactory


class ConfigLoader:
    @staticmethod
    def load_config(config_path="/app/src/config.yaml"):
        with open(config_path, "r") as file:
            return yaml.safe_load(file)


class FileAlgorithmFactory:
    @staticmethod
    def create_from_config():
        config = ConfigLoader.load_config()
        commands = []
        trains = []
        for algorithm_config in config.get("algorithms", []):
            algorithm_name = algorithm_config["name"]
            for train in algorithm_config.get("trains", []):
                file_name = train["file_name"]
                model_name = train["model_name"]
                parameters = train["parameters"]
                train = AlgorithmDataFactory.create(
                    algorithm_name, file_name, model_name, **parameters
                )
                trains.append(train)
            for execution in algorithm_config.get("executions", []):
                file_name = execution["file_name"]
                model_name = train["model_name"]
                parameters = execution["parameters"]
                command = AlgorithmDataFactory.create(
                    algorithm_name, file_name, model_name, **parameters
                )
                commands.append(command)

        return trains, commands
