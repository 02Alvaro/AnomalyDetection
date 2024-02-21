from time import time

import application.algorithms.dae.DaeExecutor
import application.algorithms.dae.DaeTrainer
from application.factories.FileAlgorithmFactory import FileAlgorithmFactory
from application.services.AlgorithmManager import AlgorithmManager


def main():
    actions = FileAlgorithmFactory.create_from_config()
    for train in actions["trains"]:
        AlgorithmManager.train(train)
    for execute in actions["tests"]:
        AlgorithmManager.execute(execute)


if __name__ == "__main__":
    t0 = time()
    main()
    t1 = time()
    print(f"Tiempo total: {round(t1 - t0, ndigits=4)} segundos")
