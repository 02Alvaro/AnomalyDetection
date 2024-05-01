import os

import numpy as np
import pandas as pd
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
output_dir = "activityTypeDataset"
file_name = "all_students_click_data_activity_type"


def pivot_and_export(group, all_days, all_activity_types):
    # Creando la tabla pivotante
    pivot_df = pd.pivot_table(group, values='sum_click', index=['date', 'id_student', 'is_anomaly'], columns='activity_type', aggfunc='sum', fill_value=0)
    
    # Reindexando las columnas para incluir todos los tipos de actividad
    pivot_df = pivot_df.reindex(columns=all_activity_types, fill_value=0)
    
    # Reestableciendo el índice para manipular las filas
    pivot_df.reset_index(inplace=True)
    
    # Creando un MultiIndex con todas las combinaciones posibles de fecha, id_student y is_anomaly
    multi_index = pd.MultiIndex.from_product([all_days, pivot_df['id_student'].unique(), pivot_df['is_anomaly'].unique()], names=['date', 'id_student', 'is_anomaly'])
    
    # Reindexando las filas para incluir todas las combinaciones de fechas y valores comunes de id_student y is_anomaly
    pivot_df.set_index(['date', 'id_student', 'is_anomaly'], inplace=True)
    pivot_df = pivot_df.reindex(multi_index, fill_value=0)
    
    # Restaurando el índice para devolver el DataFrame en un formato estándar
    pivot_df.reset_index(inplace=True)
    return pivot_df

def extract_and_transform_data():
    """
    Extrae datos de la base de datos y los transforma preparándolos para la exportación.
    """
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

    # Guardar todos los tipos de actividad y días únicos
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

def segment_data():
    """
    Divide los datos transformados en 5 segmentos y los exporta.
    """
    final_csv_path = os.path.join(output_dir, f"{file_name}.csv")
    final_df = pd.read_csv(final_csv_path)
    final_df.drop(columns=['id_student'], inplace=True)

    num_rows = len(final_df)
    segment_size = np.ceil(num_rows / 5).astype(int)

    for i in range(5):
        start_index = i * segment_size
        end_index = min((i + 1) * segment_size, num_rows)
        segment_df = final_df.iloc[start_index:end_index]
        segment_df['timestamp'] = range(1, len(segment_df) + 1)

        segment_file_name = f"{file_name}_part_{i+1}.csv"
        segment_file_path = os.path.join(output_dir, segment_file_name)

        segment_df.to_csv(segment_file_path, index=False)

def generate_exclusion_folds():
    """
    Genera archivos concatenados excluyendo uno de los segmentos en cada iteración.
    """
    archivos_partes = [f"{file_name}_part_{i}.csv" for i in range(1, 6)]

    for i in range(5):
        dfs = []
        for j, archivo in enumerate(archivos_partes):
            if i != j:
                archivo_path = os.path.join(output_dir, archivo)
                df = pd.read_csv(archivo_path)
                dfs.append(df)

        df_concatenado = pd.concat(dfs, ignore_index=True)
        df_concatenado['timestamp'] = range(1, len(df_concatenado) + 1)
        archivo_salida = f"fold_excluyendo_parte_{i+1}.csv"
        archivo_salida_path = os.path.join(output_dir, archivo_salida)

        df_concatenado.to_csv(archivo_salida_path, index=False)
        print(f"Archivo generado: {archivo_salida_path}")



if __name__ == "__main__":
    # Asegurarse de que el directorio de salida existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Paso 1: Extraer y transformar los datos
    print("Extrayendo y transformando datos...")
    extract_and_transform_data()

    # Paso 2: Segmentar los datos transformados y exportar
    print("Segmentando datos y exportando a archivos...")
    segment_data()

    # Paso 3: Generar archivos excluyendo un segmento en cada iteración
    print("Generando archivos para validación cruzada...")
    generate_exclusion_folds()

    print("Proceso completado.")


