import application.algorithms
from application.algorithms.autoencoder.AutoEncoderConfiguration import \
    AutoEncoderConfiguration
from application.algorithms.cblof.CblofConfiguration import CblofConfiguration
from application.algorithms.cof.CofConfigurator import CofConfigurator
from application.algorithms.dae.DaeConfiguration import DaeConfiguration
from application.algorithms.hbos.HbosConfiguration import HbosConfiguration
from application.algorithms.hbos.HbosTrainer import HbosTrainer
from application.algorithms.knn.KnnConfiguration import KnnConfiguration
from application.algorithms.lof.LofConfiguration import LofConfiguration
from application.algorithms.lstmVae.LstmVaeConfiguration import \
    LstmVaeConfiguration
from application.services.AlgorithmManager import AlgorithmManager


def autoencoderTutorial():
    config = AutoEncoderConfiguration(data_file="multi-dataset.csv", model_name="autoencoder.pkl", report_file="report.csv")
    AlgorithmManager.train(config)
    AlgorithmManager.evaluate(config)

def cblofTutorial():
    config = CblofConfiguration(data_file="multi-dataset.csv", model_name="cblstm.pkl", report_file="report.csv")
    AlgorithmManager.train(config)
    AlgorithmManager.evaluate(config)

def cofTutorial():
    config = CofConfigurator(data_file="multi-dataset.csv", model_name="coffe.pkl", report_file="report.csv")
    AlgorithmManager.train(config)
    AlgorithmManager.evaluate(config)

def daeTutorial():
    config = DaeConfiguration(data_file="multi-dataset.csv", model_name="daehan.pkl", report_file="report.csv")
    AlgorithmManager.train(config)
    AlgorithmManager.evaluate(config)

def hbosTutorial():
    config = HbosConfiguration(data_file="multi-dataset.csv", model_name="hbos.pkl", report_file="report.csv")
    AlgorithmManager.train(config)
    AlgorithmManager.evaluate(config)

def knnTutorial():
    config = KnnConfiguration(data_file="multi-dataset.csv", model_name="knn.pkl", report_file="report.csv")
    AlgorithmManager.train(config)
    AlgorithmManager.evaluate(config)

def lofTutorial():
    config = LofConfiguration(data_file="multi-dataset.csv", model_name="lof.pkl", report_file="report.csv")
    AlgorithmManager.train(config)
    AlgorithmManager.evaluate(config)

def lstmVaeTutorial():
    config = LstmVaeConfiguration(data_file="multi-dataset.csv", model_name="lstm_vae.pkl", report_file="report.csv")
    AlgorithmManager.train(config)
    AlgorithmManager.evaluate(config)


#importante leer DependecyContainer.py en caso de error

lofTutorial()