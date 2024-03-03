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
    def __init__(
        self,
        pyod_service: PyodWrapper,
        file_system_service: FileSystemService,
        repository: TrainRepository,
    ):
        self.pyod_service = pyod_service
        self.file_system_service = file_system_service
        self.repository = repository

    def train(self, data: LofConfiguration):
        fileData = self.file_system_service.read_dataFrom(data.data_file)

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
