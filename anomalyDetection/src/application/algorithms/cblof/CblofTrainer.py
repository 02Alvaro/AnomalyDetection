from application.algorithms.cblof.CblofData import CblofData
from application.services.AlgorithmManager import AlgorithmManager
from application.services.FileSystemService import FileSystemService
from application.services.PyodWrapper import PyodWrapper
from domain.interfaces.AlgorithmTrainer import AlgorithmTrainer
from inject import Inject
from pyod.models.cblof import CBLOF


@AlgorithmManager.trainer_for(CblofData)
@Inject
class CblofTrainer(AlgorithmTrainer):
    def __init__(
        self,
        pyod_service: PyodWrapper,
        file_system_service: FileSystemService,
    ):
        self.pyod_service = pyod_service
        self.file_system_service = file_system_service

    def train(self, data: CblofData):
        fileData = self.file_system_service.read_dataFrom(data.data_file)

        algorithm_instance = CBLOF(
            contamination=data.contamination,
            n_clusters=data.n_clusters,
            clustering_estimator=data.clustering_estimator,
            alpha=data.alpha,
            beta=data.beta,
            use_weights=data.use_weights,
            check_estimator=data.check_estimator,
            random_state=data.random_state,
        )

        algorithm_instance.fit(fileData)

        self.pyod_service.saveModel(algorithm_instance, data.model_name)
