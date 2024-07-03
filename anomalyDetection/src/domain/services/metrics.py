import numpy as np
from sklearn.metrics import confusion_matrix, roc_auc_score


def performance_metrics(y_test_binary, y_test_prediction):
    """
    Calculates performance metrics including sensitivity, specificity, precision, and ROC AUC.

    Parameters
    ----------
    y_test_binary : array-like
        Binary actual values.
    y_test_prediction : array-like
        Predicted values.

    Returns
    -------
    dict
        A dictionary containing the calculated performance metrics.
    """
    cm = confusion_matrix(y_test_binary, y_test_prediction)
    sensitivity = (
        round(cm[1, 1] / (cm[1, 0] + cm[1, 1]), ndigits=4)
        if cm[1, 0] + cm[1, 1] != 0
        else 0
    )
    specificity = (
        round(cm[0, 0] / (cm[0, 0] + cm[0, 1]), ndigits=4)
        if cm[0, 0] + cm[0, 1] != 0
        else 0
    )
    precision = (
        round(cm[1, 1] / (cm[1, 1] + cm[0, 1]), ndigits=4)
        if cm[1, 1] + cm[0, 1] != 0
        else 0
    )

    roc = "N/A"
    if len(np.unique(y_test_binary)) > 1:
        roc = round(roc_auc_score(y_test_binary, y_test_prediction), ndigits=4)

    return {"se": sensitivity, "sp": specificity, "p": precision, "roc": roc}

def file_info(csv_dataset, target_variable="is_anomaly"):
    """
    Extracts basic information from the dataset including the number of examples, dimensions, and anomaly percentage.

    Parameters
    ----------
    csv_dataset : pd.DataFrame
        The dataset to analyze.
    target_variable : str, optional
        The target variable indicating anomalies, by default "is_anomaly".

    Returns
    -------
    dict
        A dictionary containing the number of examples, number of dimensions, and anomaly percentage.
    """
    df = csv_dataset
    y = df[target_variable]
    X = df.drop(target_variable, axis=1)
    anomaly_fraction = (y == 1).sum() / len(y)

    return {
        "num_examples": X.shape[0],
        "num_dims": X.shape[1],
        "anomaly_percentage": round(anomaly_fraction * 100, ndigits=4),
    }
