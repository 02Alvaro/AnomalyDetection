from anomalyDetection.gateway.Algorithms.AlgorithmCommandFactory import AlgorithmCommandFactory

class CommandFactory:
    @staticmethod
    def create_commands_from_config(config):
        commands = []
        for algorithm_config in config.get("algorithms", []):
            algorithm_name = algorithm_config["name"]
            for execution in algorithm_config.get("executions", []):
                file_name = execution["file_name"]
                parameters = execution["parameters"] # Puedes usar esto para sobreescribir/definir parámetros específicos si es necesario.
                command = AlgorithmCommandFactory.create_command(algorithm_name, file_name, **parameters)
                commands.append(command)
        return commands
