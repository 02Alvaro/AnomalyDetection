import os

import pandas as pd
from domain.enums.PathKey import PathKey


class FileSystemService:
    def __init__(self, base_path, paths):
        self.base_path = base_path
        self.paths = paths

    def get_path(self, key: PathKey, filename: str):
        if key in self.paths:
            return os.path.join(self.base_path, self.paths[key], filename)
        else:
            raise ValueError(f"Invalid key specified: {key}")

    def read_resultsFrom(self, filename):
        file_path = self.get_path(PathKey.RESULTS, filename)
        return pd.read_csv(file_path)

    def read_dataFrom(self, filename):
        file_path = self.get_path(PathKey.DATA, filename)
        return pd.read_csv(file_path)

    def save_metricsTo(self, filename, metrics):
        file_path = self.get_path(PathKey.METRICS, filename)
        metrics.to_csv(file_path, index=False)