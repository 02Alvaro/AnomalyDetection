import os
from dataclasses import dataclass, field

import pandas as pd
import pyod
from domain.services.metrics import performance_metrics
from pyod import PyODParameters
from pyod.models.base import BaseDetector


@dataclass
class PyODParameters:
    algorithm_name: str
    contamination: float
    params: dict = field(default_factory=dict)


class PyODEWrapper:
    def __init__(self, data_path: str, results_path: str):
        self.data_path = data_path
        self.results_path = results_path

    def _get_algorithm_instance(self, params: PyODParameters) -> BaseDetector:
        # Aquí importamos dinámicamente el algoritmo basado en params.algorithm_name
        # y lo instanciamos con los parámetros proporcionados.
        algorithm_class = getattr(pyod.models, params.algorithm_name)
        return algorithm_class(**params.params)

    def execute(self, params: PyODParameters, x_train, x_test):
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
        print(metrics)

        return metrics
