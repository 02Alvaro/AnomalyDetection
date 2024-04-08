import os

import numpy as np
import pandas as pd
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
output_dir = "anomalyDetection/data"

def extract_and_transform_data():
    """
    Extrae datos de la base de datos y los transforma preparándolos para la exportación.
    """
    DAY_INCREMENT = 1  # Define el incremento de días para cada estudiante sucesivo
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
    current_day_increment = 0

    for student_id, group in vle_list.groupby("id_student"):
        df = pivot_and_export(group, student_id, all_days, all_sites)
        all_data_frames.append(df)
        current_day_increment += DAY_INCREMENT

    final_df = pd.concat(all_data_frames)
    final_csv_path = os.path.join(output_dir, "all_students_click_data.csv")
    final_df['timestamp'] = range(1, len(final_df) + 1)
    final_df.to_csv(final_csv_path, index=False)

def segment_data():
    """
    Divide los datos transformados en segmentos y los exporta.
    """
    final_csv_path = os.path.join(output_dir, "all_students_click_data.csv")
    final_df = pd.read_csv(final_csv_path)
    final_df.drop(columns=['id_student'], inplace=True)

    num_rows = len(final_df)
    segment_size = np.ceil(num_rows / 5).astype(int)

    for i in range(5):
        start_index = i * segment_size
        end_index = min((i + 1) * segment_size, num_rows)
        segment_df = final_df.iloc[start_index:end_index]

        segment_file_name = f"all_students_click_data_part_{i+1}.csv"
        segment_file_path = os.path.join(output_dir, segment_file_name)

        segment_df.to_csv(segment_file_path, index=False)

def generate_exclusion_folds():
    """
    Genera archivos concatenados excluyendo uno de los segmentos en cada iteración.
    """
    archivos_partes = [f"all_students_click_data_part_{i}.csv" for i in range(1, 6)]

    for i in range(5):
        dfs = []
        for j, archivo in enumerate(archivos_partes):
            if i != j:
                archivo_path = os.path.join(output_dir, archivo)
                df = pd.read_csv(archivo_path)
                dfs.append(df)

        df_concatenado = pd.concat(dfs, ignore_index=True)
        df_concatenado.reset_index(drop=True, inplace=True)
        df_concatenado.index += 1
        df_concatenado['timestamp'] = range(1, len(df_concatenado) + 1)
        archivo_salida = f"fold_excluyendo_parte_{i+1}.csv"
        archivo_salida_path = os.path.join(output_dir, archivo_salida)

        df_concatenado.to_csv(archivo_salida_path, index=False)
        print(f"Archivo generado: {archivo_salida_path}")

# Función auxiliar para pivotar y exportar datos
def pivot_and_export(df, student_id, all_days, all_sites):
    aggregated_df = df.groupby(["date", "id_site"])["sum_click"].sum().reset_index()
    pivot_df = aggregated_df.pivot(index="date", columns="id_site", values="sum_click").fillna(0)
    pivot_df = pivot_df.reindex(all_days, fill_value=0)
    pivot_df = pivot_df.reindex(columns=all_sites, fill_value=0)
    pivot_df.columns = [f"id_{col}" for col in pivot_df.columns]
    pivot_df.reset_index(inplace=True)
    pivot_df['id_student'] = student_id  # Añadir columna para el ID del estudiante
    pivot_df['is_anomaly'] = df['is_anomaly'].iloc[0]  # Asume que is_anomaly es constante por estudiante
    return pivot_df

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

