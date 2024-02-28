import json
import os
from dataclasses import asdict

from domain.interfaces.AlgorithmData import AlgorithmData
from domain.interfaces.TrainRepository import TrainRepository


class TrainRepositoryInFile(TrainRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, algorithmData: AlgorithmData, filename="all_models.csv"):
        header = "Algorithm,data_file,model_name,params\n"
        file_path = os.path.join(self.file_path, filename)

        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(header)

        data_dict = asdict(algorithmData)
        name = algorithmData.__class__.__name__.replace("Data", "")

        data_file = data_dict.pop("data_file")
        model_name = data_dict.pop("model_name")
        data_dict.pop("report_file")

        # Convertimos cada valor del diccionario a una cadena de texto adecuada
        processed_params = {
            k: json.dumps(v) if isinstance(v, (list, tuple)) else v
            for k, v in data_dict.items()
        }

        # Convertimos el diccionario de parámetros procesados a una cadena de texto para la columna de parámetros
        parameters_str = ";".join(f"{k}: {v}" for k, v in processed_params.items())

        # Usamos un nombre de variable diferente para evitar el conflicto
        csv_line = f"{name},{data_file},{model_name},{parameters_str}\n"

        with open(file_path, "a") as f:
            f.write(csv_line)
            print(csv_line)
