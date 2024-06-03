import os

import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import create_engine

# Script para generar un archivo CSV con los datos de los estudiantes con la media de clicks por vle


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
output_dir = "anomalyDetection/data/activity_type_clicks_sum"

def get_raw_data(code_module):
    student_list = pd.read_sql_query(
        "SELECT id_student,code_module,code_presentation,num_of_prev_attempts,studied_credits,final_result FROM StudentInfo WHERE code_module = %(code_module)s order by id_student",
        database_connection,
        params={"code_module": code_module},
    )
    vle_list = pd.read_sql_query("""
        SELECT SV.id_student, V.activity_type, sum(SV.sum_click) as sum_click 
        FROM StudentVle SV
        JOIN Vle V ON SV.id_site = V.id_site
        WHERE V.code_module = %(code_module)s 
        GROUP BY SV.id_student, V.activity_type 
        ORDER BY SV.id_student, V.activity_type;

        """,
        database_connection,
        params={"code_module": code_module},
    )
    assessment_list = pd.read_sql_query(
        "SELECT SA.id_student, SA.id_assessment,IFNULL(SA.date_submitted, -1) as date_submitted,IFNULL(SA.score, -1) as score FROM StudentAssessment SA, Assessments A WHERE A.id_assessment= SA.id_assessment and A.code_module = %(code_module)s order by SA.id_student, SA.id_assessment",
        database_connection,
        params={"code_module": code_module},
    )

    # Pivot and merge the dataframes
    assessment_list = assessment_list.pivot_table(
        index="id_student", columns="id_assessment"
    ).reset_index()
    assessment_list.columns = ["id_student"] + [
        f"{col[0]}{col[1]}" for col in assessment_list.columns[1:]
    ]

    vle_list = vle_list.pivot_table(
        index="id_student", columns="activity_type", values="sum_click"
    ).reset_index()
    vle_list.columns = ["id_student"] + [f"clicks_{i}" for i in vle_list.columns[1:]]

    # Now let's merge all the information into the student_list DataFrame
    df = pd.merge(student_list, assessment_list, on="id_student", how="left")
    df = pd.merge(df, vle_list, on="id_student", how="left")

    # Fill NaN values with -1 (or whatever value you want to use to represent 'no data')
    df.fillna(-1, inplace=True)
    return df

def get_is_anomaly(df: pd.DataFrame):
    df["is_anomaly"] = df["final_result"].replace(
        {"Fail": 1, "Withdrawn": 1, "Pass": 0, "Distinction": 0}
    )
    df.drop("final_result", axis=1, inplace=True)
    
    return df

def normalize_data(df: pd.DataFrame):
    columns_to_normalize = df.columns.difference(['id_student', 'code_module', 'code_presentation', 'num_of_prev_attempts', 'studied_credits', 'is_anomaly'])
    scaler = MinMaxScaler()
    df[columns_to_normalize] = scaler.fit_transform(df[columns_to_normalize])
    return df

def stratified_k_fold(df: pd.DataFrame, output_dir: str, file_name: str):
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
    code_modules = ['AAA', 'BBB', 'CCC', 'DDD', 'EEE', 'FFF', 'GGG']
    for code_module in code_modules:
        module_output_dir = os.path.join(output_dir, code_module)
        if not os.path.exists(module_output_dir):
            os.makedirs(module_output_dir)
        file_name = f"{code_module}_students_average_activity_type_clicks"
        df = get_raw_data(code_module)
        df.drop(["code_module", "code_presentation","id_student"], axis=1, inplace=True)
        df = get_is_anomaly(df)
        df = normalize_data(df)
        stratified_k_fold(df, module_output_dir, file_name)

if __name__ == "__main__":
    main()
