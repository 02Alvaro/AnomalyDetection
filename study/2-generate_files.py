import os

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
output_dir = "anomalyDetection/data/unique_sites_clicks"

def extract_and_transform_data():
    """
    Extracts and transforms data from the database.

    The function queries the database, processes the data, normalizes it,
    and saves the final DataFrame to a CSV file.

    Returns
    -------
    pd.DataFrame
        The final processed DataFrame containing click data for all students.
    """
    code_module = "AAA"
    query = """
    SELECT SV.date, SV.id_student, SV.id_site, SV.sum_click, 
    CASE StudentInfo.final_result
        WHEN 'Fail' THEN 1
        WHEN 'Withdrawn' THEN 1
        WHEN 'Pass' THEN 0
        WHEN 'Distinction' THEN 0
    END AS "is_anomaly"
    FROM StudentVle SV 
    JOIN StudentInfo ON StudentInfo.id_student = SV.id_student
    WHERE SV.code_module = %s
    """
    vle_list = pd.read_sql_query(query, database_connection, params=(code_module,))
    all_sites = vle_list["id_site"].unique()
    all_sites.sort()
    min_day = vle_list["date"].min()
    max_day = vle_list["date"].max()
    all_days = range(min_day, max_day + 1)
    all_data_frames = []
    for student_id, group in vle_list.groupby("id_student"):
        df = pivot_and_export(group, student_id, all_days, all_sites)
        all_data_frames.append(df)
    final_df = pd.concat(all_data_frames)
    columns_to_normalize = final_df.columns.difference(['id_student', 'date', 'is_anomaly'])
    scaler = MinMaxScaler()
    final_df[columns_to_normalize] = scaler.fit_transform(final_df[columns_to_normalize])
    final_df['timestamp'] = range(1, len(final_df) + 1)
    final_csv_path = os.path.join(output_dir, "all_students_click_data.csv")
    final_df.to_csv(final_csv_path, index=False)
    return final_df

def pivot_and_export(df, student_id, all_days, all_sites):
    """
    Pivots and exports individual student click data.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing click data for a single student.
    student_id : int
        The ID of the student.
    all_days : range
        Range of all days to reindex the DataFrame.
    all_sites : np.ndarray
        Array of all unique site IDs to reindex the DataFrame.

    Returns
    -------
    pd.DataFrame
        The pivoted and processed DataFrame for the student.
    """
    aggregated_df = df.groupby(["date", "id_site"])["sum_click"].sum().reset_index()
    pivot_df = aggregated_df.pivot(index="date", columns="id_site", values="sum_click").fillna(0)
    pivot_df = pivot_df.reindex(all_days, fill_value=0)
    pivot_df = pivot_df.reindex(columns=all_sites, fill_value=0)
    pivot_df.columns = [f"id_{col}" for col in pivot_df.columns]
    pivot_df.reset_index(inplace=True)
    pivot_df['id_student'] = student_id
    pivot_df['is_anomaly'] = df['is_anomaly'].iloc[0]
    return pivot_df

def stratified_k_fold(final_df):
    """
    Applies Stratified K-Fold cross-validation and exports the folds to CSV files.

    Parameters
    ----------
    final_df : pd.DataFrame
        The final processed DataFrame containing click data for all students.
    """
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
