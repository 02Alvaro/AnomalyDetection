from application.services.AlgorithmDataProcesor import AlgorithmDataProcesor
from application.services.FileSystemService import FileSystemService
from application.services.PyodWrapper import PyodWrapper
from application.services.TimeEvalWrapper import TimeEvalWrapper
from domain.enums.PathKey import PathKey
from domain.interfaces.EvaluationRepository import EvaluationRepository
from infrastructure.repository.EvaluationRepositoryInFile import (
    EvaluationRepositoryInFile,
)


class DependencyContainer:
    services = {}

    @classmethod
    def add_service(cls, service_type, instance):
        cls.services[service_type] = instance

    @classmethod
    def get_service(cls, service_type):
        return cls.services.get(service_type)


# Cualquier elemento que utilice docker, necesita el path de host para hacer un mapeo con volumenes
HOST = "E:/AnomalyDetection/anomalyDetection"
DOCKER = "/app"

paths = {
    PathKey.RESULTS: "results",
    PathKey.DATA: "data",
    PathKey.METRICS: "metrics",
}

DependencyContainer.add_service(
    EvaluationRepository,
    EvaluationRepositoryInFile(DOCKER + "/" + paths[PathKey.METRICS]),
)

DependencyContainer.add_service(
    TimeEvalWrapper,
    TimeEvalWrapper(
        HOST + "/" + paths[PathKey.DATA], HOST + "/" + paths[PathKey.RESULTS]
    ),
)

DependencyContainer.add_service(
    FileSystemService, FileSystemService(DOCKER, paths=paths)
)

DependencyContainer.add_service(
    AlgorithmDataProcesor,
    AlgorithmDataProcesor(DependencyContainer.get_service(FileSystemService)),
)

DependencyContainer.add_service(
    PyodWrapper,
    PyodWrapper(DependencyContainer.get_service(FileSystemService)),
)
