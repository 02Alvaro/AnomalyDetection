from application.algorithms.cof.CofData import CofData
from application.services.AlgorithmManager import AlgorithmManager
from application.services.FileSystemService import FileSystemService
from application.services.PyodWrapper import PyodWrapper
from domain.interfaces.AlgorithmTrainer import AlgorithmTrainer
from inject import Inject
from pyod.models.cof import COF


@AlgorithmManager.trainer_for(CofData)
@Inject
class CofTrainer(AlgorithmTrainer):
    def __init__(
        self,
        pyod_service: PyodWrapper,
        file_system_service: FileSystemService,
    ):
        self.pyod_service = pyod_service
        self.file_system_service = file_system_service

    def train(self, data: CofData):
        fileData = self.file_system_service.read_dataFrom(data.data_file)

        algorithm_instance = COF(
            contamination=data.contamination,
            n_neighbors=data.n_neighbors,
            method=data.method,
        )

        algorithm_instance.fit(fileData)

        self.pyod_service.saveModel(algorithm_instance, data.model_name)
