from time import time

from application.factories.FileAlgorithmFactory import FileAlgorithmFactory
from application.services.AlgorithmManager import AlgorithmManager

import application.algorithms


def main():
    [trains, executes] = FileAlgorithmFactory.create_from_config()
    for train in trains:
        AlgorithmManager.train(train)
    for execute in executes:
        AlgorithmManager.execute(execute)


if __name__ == "__main__":
    t0 = time()
    main()
    t1 = time()
    print(f"Tiempo total: {round(t1 - t0, ndigits=4)} segundos")
