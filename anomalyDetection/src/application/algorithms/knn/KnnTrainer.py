from application.algorithms.knn.KnnConfiguration import KnnConfiguration
from application.services.AlgorithmManager import AlgorithmManager
from application.services.FileSystemService import FileSystemService
from application.services.PyodWrapper import PyodWrapper
from domain.interfaces.AlgorithmTrainer import AlgorithmTrainer
from domain.interfaces.TrainRepository import TrainRepository
from inject import Inject
from pyod.models.knn import KNN


@AlgorithmManager.trainer_for(KnnConfiguration)
@Inject
class KnnTrainer(AlgorithmTrainer):
    """
    Trainer class for the KNN algorithm.

    Attributes
    ----------
    pyod_service : PyodWrapper
        Wrapper for the PyOD library.
    file_system_service : FileSystemService
        Service for file system operations.
    repository : TrainRepository
        Repository for storing training data.
    """

    def __init__(
        self,
        pyod_service: PyodWrapper,
        file_system_service: FileSystemService,
        repository: TrainRepository,
    ):
        """
        Initializes the KNN trainer with the provided services.

        Parameters
        ----------
        pyod_service : PyodWrapper
            Wrapper for the PyOD library.
        file_system_service : FileSystemService
            Service for file system operations.
        repository : TrainRepository
            Repository for storing training data.
        """
        self.pyod_service = pyod_service
        self.file_system_service = file_system_service
        self.repository = repository

    def train(self, data: KnnConfiguration):
        """
        Trains the KNN algorithm with the given configuration.

        Parameters
        ----------
        data : KnnConfiguration
            Configuration data for the KNN algorithm.

        Returns
        -------
        None
        """
        fileData = self.file_system_service.read_dataFrom(data.data_file)

        algorithm_instance = KNN(
            contamination=data.contamination,
            n_neighbors=data.n_neighbors,
            radius=data.radius,
            algorithm=data.algorithm,
            leaf_size=data.leaf_size,
            metric=data.metric,
            p=data.p,
            metric_params=data.metric_params,
            n_jobs=data.n_jobs,
        )
        algorithm_instance.fit(fileData)

        self.pyod_service.saveModel(algorithm_instance, data.model_name)

        self.repository.save(data)
