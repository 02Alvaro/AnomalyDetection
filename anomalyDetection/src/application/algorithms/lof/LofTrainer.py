from application.algorithms.lof.LofConfiguration import LofConfiguration
from application.services.AlgorithmManager import AlgorithmManager
from application.services.FileSystemService import FileSystemService
from application.services.PyodWrapper import PyodWrapper
from domain.interfaces.AlgorithmTrainer import AlgorithmTrainer
from domain.interfaces.TrainRepository import TrainRepository
from inject import Inject
from pyod.models.lof import LOF as LOF


@AlgorithmManager.trainer_for(LofConfiguration)
@Inject
class LofTrainer(AlgorithmTrainer):
    """
    Trainer class for the LOF algorithm.

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
        Initializes the LOF trainer with the provided services.

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

    def train(self, data: LofConfiguration):
        """
        Trains the LOF algorithm with the given configuration.

        Parameters
        ----------
        data : LofConfiguration
            Configuration data for the LOF algorithm.

        Returns
        -------
        None
        """
        fileData = self.file_system_service.read_dataFrom(data.data_file)
        
        # Eliminate the "is_anomaly" column if it exists
        if "is_anomaly" in fileData.columns:
            fileData = fileData.drop(columns=["is_anomaly"])

        algorithm_instance = LOF(
            n_neighbors=data.n_neighbors,
            algorithm=data.algorithm,
            leaf_size=data.leaf_size,
            metric=data.metric,
            p=data.p,
            metric_params=data.metric_params,
            contamination=data.contamination,
            n_jobs=data.n_jobs,
            novelty=data.novelty,
        )

        algorithm_instance.fit(fileData)

        self.pyod_service.saveModel(algorithm_instance, data.model_name)

        self.repository.save(data)
