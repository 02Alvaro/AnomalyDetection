import os
from dataclasses import dataclass, field

from application.services.FileSystemService import FileSystemService
from joblib import dump, load


@dataclass
class PyodParameters:
    algorithm_name: str
    contamination: float
    params: dict = field(default_factory=dict)


class PyodWrapper:

    def __init__(
        self,
        file_system_service: FileSystemService,
    ):
        self.file_system_service = file_system_service

    def saveModel(self, model, filename):
        dump(
            model,
            os.path.join(self.file_system_service.get_results_path(), filename),
            protocol=4,
        )

    def loadModel(self, filename):
        return load(
            os.path.join(self.file_system_service.get_results_path(), filename))
