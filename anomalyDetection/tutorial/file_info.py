import pandas as pd


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


def main():
    file_name = "anomalyDetection/data/multi-dataset.csv"

    df = pd.read_csv(file_name)
    print(file_info(df))

if __name__ == "__main__":
    main()