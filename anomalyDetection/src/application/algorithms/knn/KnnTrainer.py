from application.algorithms.knn.KnnData import KnnData
from application.services.AlgorithmManager import AlgorithmManager
from application.services.FileSystemService import FileSystemService
from application.services.PyodWrapper import PyodWrapper
from domain.interfaces.AlgorithmTrainer import AlgorithmTrainer
from inject import Inject
from pyod.models.knn import KNN


@AlgorithmManager.trainer_for(KnnData)
@Inject
class CofTrainer(AlgorithmTrainer):
    def __init__(
        self,
        pyod_service: PyodWrapper,
        file_system_service: FileSystemService,
    ):
        self.pyod_service = pyod_service
        self.file_system_service = file_system_service

    def train(self, data: KnnData):
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
