import os

import pandas as pd
from sklearn.model_selection import StratifiedKFold


def stratified_k_fold(df: pd.DataFrame, output_dir: str):
    skf = StratifiedKFold(n_splits=5)
    X = df.drop('is_anomaly', axis=1)
    y = df['is_anomaly']
    
    fold_number = 1
    for train_index, test_index in skf.split(X, y):
        train_df = df.iloc[train_index]
        test_df = df.iloc[test_index]
        train_no_anomaly_df = train_df[train_df['is_anomaly'] == 0]
        
        train_path = os.path.join(output_dir, f"train_fold_{fold_number}.csv")
        test_path = os.path.join(output_dir, f"test_fold_{fold_number}.csv")
        train_no_anomaly_path = os.path.join(output_dir, f"train_no_anomaly_fold_{fold_number}.csv")
        
        train_df.to_csv(train_path, index=False)
        test_df.to_csv(test_path, index=False)
        train_no_anomaly_df.to_csv(train_no_anomaly_path, index=False)
        
        fold_number += 1

def main():
    base_path = "anomalyDetection"
    module_output_dir = "tutorial/output/partitioning"
    module_path = os.path.join(base_path, module_output_dir)
    file = os.path.join(base_path,"data", "multi-dataset.csv")

    if not os.path.exists(module_path):
        os.makedirs(module_path)
    
    df = pd.read_csv(file)
    stratified_k_fold(df, module_path)

if __name__ == "__main__":
    main()