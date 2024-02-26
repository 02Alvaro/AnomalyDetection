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

    def _get_algorithm_instance(self, params: PyodParameters) -> BaseDetector:
        # Aquí importamos dinámicamente el algoritmo basado en params.algorithm_name
        # y lo instanciamos con los parámetros proporcionados.
        algorithm_class = getattr(pyod.models, params.algorithm_name)
        return algorithm_class(**params.params)

    def execute(self, params: PyodParameters, x_train, x_test):
        # Crear una instancia del algoritmo
        clf = self._get_algorithm_instance(params)

        # Entrenar el modelo
        clf.fit(x_train)

        # Guardar resultados, por ejemplo, puntuaciones de anomalía
        y_test_scores = clf.decision_function(x_test)
        results_file = os.path.join(
            self.results_path, f"{params.algorithm_name}_scores.csv"
        )
        pd.DataFrame(y_test_scores).to_csv(results_file, index=False)

        return results_file

    def evaluate_performance(self, y_true, y_scores_csv):
        # Cargar puntuaciones de anomalía
        y_test_scores = pd.read_csv(y_scores_csv)

        # Supongamos que el umbral se calcula o se define de antemano
        threshold = 0.5
        y_test_pred = [1 if score > threshold else 0 for score in y_test_scores]

        # Calcular métricas de rendimiento
        metrics = performance_metrics(y_true, y_test_pred)

        return metrics

    def saveModel(self, model, filename):
        dump(model, os.path.join(self.file_system_service.get_results_path(), filename))

    def loadModel(self, filename):
        return load(os.path.join(self.file_system_service.get_results_path(), filename))
