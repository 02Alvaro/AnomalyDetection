import os
from dataclasses import dataclass, field

import pandas as pd
import pyod
from application.services.FileSystemService import FileSystemService
from domain.services.metrics import performance_metrics
from joblib import dump, load
from pyod.models.base import BaseDetector


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
        dump(model, os.path.join(self.file_system_service.get_results_path(), filename))

    def loadModel(self, filename):
        return load(os.path.join(self.file_system_service.get_results_path(), filename))
