"""
Este módulo proporciona tutoriales para configurar y evaluar diversos algoritmos de aprendizaje automático utilizando el `AlgorithmManager` de la aplicación.

Clases y Métodos:
-----------------
- autoencoderTutorial:
    Configura y evalúa un modelo AutoEncoder con el archivo de datos `multi-dataset.csv`.

- cblofTutorial:
    Configura y evalúa un modelo CBLOF con el archivo de datos `multi-dataset.csv`.

- cofTutorial:
    Configura y evalúa un modelo COF con el archivo de datos `multi-dataset.csv`.

- daeTutorial:
    Configura y evalúa un modelo DAE con el archivo de datos `multi-dataset.csv`.

- hbosTutorial:
    Configura y evalúa un modelo HBOS con el archivo de datos `multi-dataset.csv`.

- knnTutorial:
    Configura y evalúa un modelo KNN con el archivo de datos `multi-dataset.csv`.

- lofTutorial:
    Configura y evalúa un modelo LOF con el archivo de datos `multi-dataset.csv`.

- lstmVaeTutorial:
    Configura y evalúa un modelo LSTM-VAE con el archivo de datos `multi-dataset.csv`.

Nota:
-----
En caso de error, se recomienda revisar el archivo `DependencyContainer.py` para verificar dependencias y configuraciones adicionales necesarias.

Ejemplo de uso:
---------------
Para utilizar el tutorial de LOF, simplemente llame al método correspondiente:
    lofTutorial()
"""
import application.algorithms
from application.algorithms.autoencoder.AutoEncoderConfiguration import AutoEncoderConfiguration
from application.algorithms.cblof.CblofConfiguration import CblofConfiguration
from application.algorithms.cof.CofConfigurator import CofConfigurator
from application.algorithms.dae.DaeConfiguration import DaeConfiguration
from application.algorithms.hbos.HbosConfiguration import HbosConfiguration
from application.algorithms.hbos.HbosTrainer import HbosTrainer
from application.algorithms.knn.KnnConfiguration import KnnConfiguration
from application.algorithms.lof.LofConfiguration import LofConfiguration
from application.algorithms.lstmVae.LstmVaeConfiguration import LstmVaeConfiguration
from application.services.AlgorithmManager import AlgorithmManager

def autoencoderTutorial():
    """
    Configura y entrena un modelo AutoEncoder y genera un reporte de evaluación.

    - Archivo de datos: multi-dataset.csv
    - Modelo: autoencoder.pkl
    - Reporte: report.csv
    """
    config = AutoEncoderConfiguration(data_file="multi-dataset.csv", model_name="autoencoder.pkl", report_file="report.csv")
    AlgorithmManager.train(config)
    AlgorithmManager.evaluate(config)

def cblofTutorial():
    """
    Configura y entrena un modelo CBLOF y genera un reporte de evaluación.

    - Archivo de datos: multi-dataset.csv
    - Modelo: cblstm.pkl
    - Reporte: report.csv
    """
    config = CblofConfiguration(data_file="multi-dataset.csv", model_name="cblstm.pkl", report_file="report.csv")
    AlgorithmManager.train(config)
    AlgorithmManager.evaluate(config)

def cofTutorial():
    """
    Configura y entrena un modelo COF y genera un reporte de evaluación.

    - Archivo de datos: multi-dataset.csv
    - Modelo: coffe.pkl
    - Reporte: report.csv
    """
    config = CofConfigurator(data_file="multi-dataset.csv", model_name="coffe.pkl", report_file="report.csv")
    AlgorithmManager.train(config)
    AlgorithmManager.evaluate(config)

def daeTutorial():
    """
    Configura y entrena un modelo DAE y genera un reporte de evaluación.

    - Archivo de datos: multi-dataset.csv
    - Modelo: daehan.pkl
    - Reporte: report.csv
    """
    config = DaeConfiguration(data_file="multi-dataset.csv", model_name="daehan.pkl", report_file="report.csv")
    AlgorithmManager.train(config)
    AlgorithmManager.evaluate(config)

def hbosTutorial():
    """
    Configura y entrena un modelo HBOS y genera un reporte de evaluación.

    - Archivo de datos: multi-dataset.csv
    - Modelo: hbos.pkl
    - Reporte: report.csv
    """
    config = HbosConfiguration(data_file="multi-dataset.csv", model_name="hbos.pkl", report_file="report.csv")
    AlgorithmManager.train(config)
    AlgorithmManager.evaluate(config)

def knnTutorial():
    """
    Configura y entrena un modelo KNN y genera un reporte de evaluación.

    - Archivo de datos: multi-dataset.csv
    - Modelo: knn.pkl
    - Reporte: report.csv
    """
    config = KnnConfiguration(data_file="multi-dataset.csv", model_name="knn.pkl", report_file="report.csv")
    AlgorithmManager.train(config)
    AlgorithmManager.evaluate(config)

def lofTutorial():
    """
    Configura y entrena un modelo LOF y genera un reporte de evaluación.

    - Archivo de datos: multi-dataset.csv
    - Modelo: lof.pkl
    - Reporte: report.csv
    """
    config = LofConfiguration(data_file="multi-dataset.csv", model_name="lof.pkl", report_file="report.csv")
    AlgorithmManager.train(config)
    AlgorithmManager.evaluate(config)

def lstmVaeTutorial():
    """
    Configura y entrena un modelo LSTM-VAE y genera un reporte de evaluación.

    - Archivo de datos: multi-dataset.csv
    - Modelo: lstm_vae.pkl
    - Reporte: report.csv
    """
    config = LstmVaeConfiguration(data_file="multi-dataset.csv", model_name="lstm_vae.pkl", report_file="report.csv")
    AlgorithmManager.train(config)
    AlgorithmManager.evaluate(config)

# Importante leer DependencyContainer.py en caso de error
#lofTutorial()
