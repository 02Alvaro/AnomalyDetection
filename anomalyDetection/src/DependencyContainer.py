from application.services.AlgorithmDataProcesor import AlgorithmDataProcesor
from application.services.FileSystemService import FileSystemService
from application.services.PyodWrapper import PyodWrapper
from application.services.TimeEvalWrapper import TimeEvalWrapper
from domain.enums.PathKey import PathKey
from domain.interfaces.ReportInterface import ReportInterface
from domain.interfaces.TrainRepository import TrainRepository
from infrastructure.repository.ReportInFile import ReportInFile
from infrastructure.repository.TrainRepositoryInFile import \
    TrainRepositoryInFile


class DependencyContainer:
    """
    Container for managing service dependencies.

    Attributes
    ----------
    services : dict
        Dictionary to store service instances.
    """

    services = {}

    @classmethod
    def add_service(cls, service_type, instance):
        """
        Adds a service instance to the container.

        Parameters
        ----------
        service_type : type
            The type of the service.
        instance : object
            The instance of the service.
        """
        cls.services[service_type] = instance

    @classmethod
    def get_service(cls, service_type):
        """
        Retrieves a service instance from the container.

        Parameters
        ----------
        service_type : type
            The type of the service.

        Returns
        -------
        object
            The instance of the requested service, or None if not found.
        """
        return cls.services.get(service_type)


# Cualquier elemento que utilice docker, necesita el path de host para hacer un mapeo con volúmenes
HOST = "E:/AnomalyDetection/anomalyDetection"
#HOST = "/mnt/e/AnomalyDetection/anomalyDetection"
DOCKER = "/app"
# Si se ejecuta sin docker, se debe de descomentar la siguiente linea
DOCKER = HOST

paths = {
    PathKey.RESULTS: "results",
    PathKey.DATA: "data",
    PathKey.METRICS: "metrics",
}

DependencyContainer.add_service(
    ReportInterface,
    ReportInFile(DOCKER + "/" + paths[PathKey.METRICS]),
)

DependencyContainer.add_service(
    TrainRepository,
    TrainRepositoryInFile(DOCKER + "/" + paths[PathKey.RESULTS]),
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
