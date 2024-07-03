from application.algorithms.cblof.CblofConfiguration import CblofConfiguration
from application.services.AlgorithmManager import AlgorithmManager
from application.services.FileSystemService import FileSystemService
from application.services.PyodWrapper import PyodWrapper
from domain.interfaces.AlgorithmTrainer import AlgorithmTrainer
from domain.interfaces.TrainRepository import TrainRepository
from inject import Inject
from pyod.models.cblof import CBLOF


@AlgorithmManager.trainer_for(CblofConfiguration)
@Inject
class CblofTrainer(AlgorithmTrainer):
    """
    Trainer class for the CBLOF algorithm.

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
        Initializes the CBLOF trainer with the provided services.

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

    def train(self, data: CblofConfiguration):
        """
        Trains the CBLOF algorithm with the given configuration.

        Parameters
        ----------
        data : CblofConfiguration
            Configuration data for the CBLOF algorithm.

        Returns
        -------
        None
        """
        fileData = self.file_system_service.read_dataFrom(data.data_file)

        algorithm_instance = CBLOF(
            contamination=data.contamination,
            n_clusters=data.n_clusters,
            clustering_estimator=data.clustering_estimator,
            alpha=data.alpha,
            beta=data.beta,
            use_weights=data.use_weights,
            check_estimator=data.check_estimator,
            random_state=data.seed,
        )

        algorithm_instance.fit(fileData)

        self.pyod_service.saveModel(algorithm_instance, data.model_name)

        self.repository.save(data)
