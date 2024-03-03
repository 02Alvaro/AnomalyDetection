from domain.exceptions.AlgorithmNotFound import AlgorithmDataNotFound
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


class AlgorithmFactory:
    algorithm_config = {}

    @staticmethod
    def Configurator_for(name):
        def decorator(cls):
            AlgorithmFactory.algorithm_config[name] = cls
            return cls

        return decorator

    @staticmethod
    def create(name, data_file, **kwargs):
        data_class: AlgorithmConfigurator = AlgorithmFactory.algorithm_config.get(name)
        if not data_class:
            raise AlgorithmDataNotFound(name)

        return data_class(data_file=data_file, **kwargs)
