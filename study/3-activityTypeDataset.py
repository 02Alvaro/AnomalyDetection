import os

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import create_engine

# Configuración de la base de datos
database_username = "root"
database_password = "anomaly"
database_ip = "localhost"
database_port = "3306"
database_name = "OpenUniversityData"
database_connection = create_engine(
    f"mysql+pymysql://{database_username}:{database_password}@{database_ip}:{database_port}/{database_name}"
)

# Directorio de salida para todos los archivos generados
output_dir = "anomalyDetection/data/activity_type_clicks"
file_name = "all_students_click_data_activity_type"

def pivot_and_export(group, all_days, all_activity_types):
    pivot_df = pd.pivot_table(group, values='sum_click', index=['date', 'id_student', 'is_anomaly'], columns='activity_type', aggfunc='sum', fill_value=0)
    pivot_df = pivot_df.reindex(columns=all_activity_types, fill_value=0)
    pivot_df.reset_index(inplace=True)
    multi_index = pd.MultiIndex.from_product([all_days, pivot_df['id_student'].unique(), pivot_df['is_anomaly'].unique()], names=['date', 'id_student', 'is_anomaly'])
    pivot_df.set_index(['date', 'id_student', 'is_anomaly'], inplace=True)
    pivot_df = pivot_df.reindex(multi_index, fill_value=0)
    pivot_df.reset_index(inplace=True)
    return pivot_df

def extract_and_transform_data():
    code_module = "AAA"
    query = """
    SELECT SV.date, SV.id_student,Vle.activity_type, Sum( SV.sum_click) as 'sum_click',
    CASE StudentInfo.final_result
        WHEN 'Fail' THEN 1
        WHEN 'Withdrawn' THEN 1
        WHEN 'Pass' THEN 0
        WHEN 'Distinction' THEN 0
    END AS "is_anomaly"
    FROM StudentVle SV 
    JOIN StudentInfo ON StudentInfo.id_student = SV.id_student
    JOIN Vle ON Vle.id_site = SV.id_site
    WHERE SV.code_module = %s
    GROUP BY SV.date, SV.id_student,StudentInfo.final_result,Vle.activity_type;
    """
    vle_list = pd.read_sql_query(query, database_connection, params=(code_module,))
    vle_list = vle_list.astype({"date": "int32", "id_student": "int32", "sum_click": "int32"})
    all_activity_types = vle_list["activity_type"].unique()
    all_activity_types.sort()
    min_day = vle_list["date"].min()
    max_day = vle_list["date"].max()
    all_days = range(min_day, max_day + 1)
    all_students = []
    for student_id, group in vle_list.groupby("id_student"):
        df = pivot_and_export(group, all_days, all_activity_types)
        all_students.append(df)
    final_df = pd.concat(all_students)
    final_csv_path = os.path.join(output_dir, f"{file_name}.csv")
    columns_to_normalize = final_df.columns.difference(['id_student', 'timestamp', 'is_anomaly', 'date', 'activity_type'])
    scaler = MinMaxScaler()
    final_df[columns_to_normalize] = scaler.fit_transform(final_df[columns_to_normalize])
    final_df['timestamp'] = range(1, len(final_df) + 1)
    final_df.to_csv(final_csv_path, index=False)
    return final_df

def stratified_k_fold(final_df):
    skf = StratifiedKFold(n_splits=5)
    X = final_df.drop(['is_anomaly'], axis=1)
    y = final_df['is_anomaly']
    fold_number = 1
    for train_index, test_index in skf.split(X, y):
        train_df = final_df.iloc[train_index]
        test_df = final_df.iloc[test_index]
        train_path = os.path.join(output_dir, f"train_fold_{fold_number}.csv")
        test_path = os.path.join(output_dir, f"test_fold_{fold_number}.csv")
        train_df.to_csv(train_path, index=False)
        test_df.to_csv(test_path, index=False)
        print(f"Train fold {fold_number} and Test fold {fold_number} generated.")
        fold_number += 1

if __name__ == "__main__":
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print("Extrayendo y transformando datos...")
    final_df = extract_and_transform_data()
    print("Aplicando Stratified K-Fold y exportando...")
    stratified_k_fold(final_df)
    print("Proceso completado.")
