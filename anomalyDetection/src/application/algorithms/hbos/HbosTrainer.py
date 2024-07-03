from application.algorithms.hbos.HbosConfiguration import HbosConfiguration
from application.services.AlgorithmManager import AlgorithmManager
from application.services.FileSystemService import FileSystemService
from application.services.PyodWrapper import PyodWrapper
from domain.interfaces.AlgorithmTrainer import AlgorithmTrainer
from domain.interfaces.TrainRepository import TrainRepository
from inject import Inject
from pyod.models.hbos import HBOS


@AlgorithmManager.trainer_for(HbosConfiguration)
@Inject
class HbosTrainer(AlgorithmTrainer):
    """
    Trainer class for the HBOS algorithm.

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
        Initializes the HBOS trainer with the provided services.

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

    def train(self, data: HbosConfiguration):
        """
        Trains the HBOS algorithm with the given configuration.

        Parameters
        ----------
        data : HbosConfiguration
            Configuration data for the HBOS algorithm.

        Returns
        -------
        None
        """
        fileData = self.file_system_service.read_dataFrom(data.data_file)

        algorithm_instance = HBOS(
            contamination=data.contamination,
            n_bins=data.n_bins,
            alpha=data.alpha,
            tol=data.tol,
        )

        algorithm_instance.fit(fileData)

        self.pyod_service.saveModel(algorithm_instance, data.model_name)

        self.repository.save(data)
