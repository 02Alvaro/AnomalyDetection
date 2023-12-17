from domain.exceptions.AlgorithmNotFound import AlgorithmDataNotFound
from domain.interfaces.AlgorithmData import AlgorithmData


class AlgorithmDataFactory:
    data_classes = {}

    @staticmethod
    def dataClass_for(name):
        def decorator(cls):
            AlgorithmDataFactory.data_classes[name] = cls
            return cls

        return decorator

    @staticmethod
    def create(name, data_file, **kwargs):
        data_class: AlgorithmData = AlgorithmDataFactory.data_classes.get(name)
        if not data_class:
            raise AlgorithmDataNotFound(name)

        return data_class(data_file=data_file, **kwargs)
