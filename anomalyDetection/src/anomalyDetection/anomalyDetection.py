import os
import numpy as np
import pandas as pd
from time import time
from sklearn.model_selection import train_test_split
from pyod.models.cblof import CBLOF
from pyod.models.hbos import HBOS
from pyod.models.knn import KNN
from pyod.models.lof import LOF
from pyod.models.cof import COF
from pyod.utils.utility import standardizer
from sklearn.metrics import confusion_matrix, roc_auc_score
from joblib import Parallel, delayed

def randomize():
    return np.random.randint(5, 100)

def instantiate_clfs(classifiers_parameters, anomaly_fraction, random_state=None):
    classifiers = {
        'COF': COF(contamination=anomaly_fraction, n_neighbors=classifiers_parameters.get('COF', randomize())),
        'KNN': KNN(contamination=anomaly_fraction, n_neighbors=classifiers_parameters.get('KNN', randomize())),
        'CBLOF': CBLOF(contamination=anomaly_fraction, check_estimator=False, random_state=random_state, n_clusters=classifiers_parameters.get('CBLOF', randomize())),
        'HBOS': HBOS(contamination=anomaly_fraction, n_bins=classifiers_parameters.get('HBOS', randomize())),
        'LOF': LOF(contamination=anomaly_fraction, n_neighbors=classifiers_parameters.get('LOF', randomize()))
    }
    return classifiers


def compare_predictions(y_values,y_predictions):
    count = {}
    for actual,pred in zip( y_values,y_predictions):
        count[(actual,pred)] = count.get((actual,pred), 0) + 1
    return count


def performance_metrics(y_test_binary, y_test_prediction):

    cm = confusion_matrix(y_test_binary, y_test_prediction)
    sensitivity = round(cm[1, 1] / (cm[1, 0] + cm[1, 1]), ndigits=4) if cm[1, 0] + cm[1, 1] != 0 else 0
    specificity = round(cm[0, 0] / (cm[0, 0] + cm[0, 1]), ndigits=4) if cm[0, 0] + cm[0, 1] != 0 else 0
    precision = round(cm[1, 1] / (cm[1, 1] + cm[0, 1]), ndigits=4) if cm[1, 1] + cm[0, 1] != 0 else 0
    roc = round(roc_auc_score(y_test_binary, y_test_prediction), ndigits=4)


    return {"se": sensitivity, "sp": specificity, "p": precision, "roc": roc}


def train_and_evaluate(clf, x_train_norm, x_test_norm, y_test):
    t0 = time()
    clf.fit(x_train_norm)
    y_test_pred = clf.predict(x_test_norm)
    t1 = time()
    metrics = performance_metrics((y_test == 1).astype(int), y_test_pred)
    metrics['cm'] = compare_predictions(y_test, y_test_pred) #TODO
    metrics['time'] = round(t1 - t0, ndigits=4)
    metrics['clf'] = clf.__class__.__name__
    return metrics

def load_and_preprocess_data(csv_dataset, random_state, target_variable):
    df = pd.read_csv(os.path.join(os.getcwd(), 'coursesData', csv_dataset))
    df.drop(['code_module', 'code_presentation', 'id_student'], axis=1, inplace=True)
    y = df[target_variable].replace({
        'Fail': 0,
        'Withdrawn': 1,
        'Pass': 2,
        'Distinction': 3
    })
    X = df.drop(target_variable, axis=1)
    anomaly_fraction = (y == 1).sum() / len(y)
    x_train, x_test, _, y_test = train_test_split(X, y, test_size=0.3, random_state=random_state)
    x_train_norm, x_test_norm = standardizer(x_train, x_test)
    return x_train_norm, x_test_norm, y_test, anomaly_fraction

def process_dataset(csv_dataset,classifiers_parameters, random_state, target_variable):

    x_train_norm, x_test_norm, y_test, anomaly_fraction = load_and_preprocess_data(csv_dataset, random_state, target_variable)

    classifiers = instantiate_clfs(classifiers_parameters,anomaly_fraction,random_state)

    all_clf_metrics = Parallel(n_jobs=-1)(delayed(train_and_evaluate)(clf, x_train_norm, x_test_norm, y_test) for clf_name, clf in classifiers.items())

    return csv_dataset[:-4], x_train_norm.shape[0], x_train_norm.shape[1], round(anomaly_fraction * 100, ndigits=4), all_clf_metrics

