import argparse
import sys
from time import time

import application.algorithms
from application.factories.AlgorithmFileConfigurationFactory import (
    AlgorithmFileConfigurationFactory, ConfigLoader)
from application.services.AlgorithmManager import AlgorithmManager
from joblib import Parallel, delayed


def parse_arguments():
    """
    Parses command line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Ejecuta algoritmos basados en una configuración."
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="Ruta del archivo de configuración YAML.",
    )
    return parser.parse_args()

# Importante leer DependencyContainer.py en caso de error

def main(config_path):
    """
    Main function to execute algorithms based on the configuration file.

    Parameters
    ----------
    config_path : str
        Path to the configuration YAML file.
    """
    config_loader = ConfigLoader(config_path)
    algorithm_factory = AlgorithmFileConfigurationFactory(config_loader)
    actions = algorithm_factory.create_from_config()

    Parallel(n_jobs=-1)(
        delayed(AlgorithmManager.train)(train) for train in actions["trains"]
    )
    Parallel(n_jobs=-1)(
        delayed(AlgorithmManager.evaluate)(execute) for execute in actions["tests"]
    )

if __name__ == "__main__":
    args = parse_arguments()
    t0 = time()
    main(args.file)
    t1 = time()
    print(f"Tiempo total: {round(t1 - t0, ndigits=4)} segundos")
