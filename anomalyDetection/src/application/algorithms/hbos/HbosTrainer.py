from application.algorithms.hbos.HbosData import HbosData
from application.services.AlgorithmManager import AlgorithmManager
from application.services.FileSystemService import FileSystemService
from application.services.PyodWrapper import PyodWrapper
from domain.interfaces.AlgorithmTrainer import AlgorithmTrainer
from inject import Inject
from pyod.models.hbos import HBOS


@AlgorithmManager.trainer_for(HbosData)
@Inject
class HbosTrainer(AlgorithmTrainer):
    def __init__(
        self,
        pyod_service: PyodWrapper,
        file_system_service: FileSystemService,
    ):
        self.pyod_service = pyod_service
        self.file_system_service = file_system_service

    def train(self, data: HbosData):
        fileData = self.file_system_service.read_dataFrom(data.data_file)

        algorithm_instance = HBOS(
            contamination=data.contamination,
            n_bins=data.n_bins,
            alpha=data.alpha,
            tol=data.tol,
        )

        algorithm_instance.fit(fileData)

        self.pyod_service.saveModel(algorithm_instance, data.model_name)
