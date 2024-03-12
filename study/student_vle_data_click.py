import os

import pandas as pd
from sqlalchemy import create_engine

database_username = "root"
database_password = "anomaly"
database_ip = "localhost"
database_port = "3306"
database_name = "OpenUniversityData"
database_connection = create_engine(
    f"mysql+pymysql://{database_username}:{database_password}@{database_ip}:{database_port}/{database_name}"
)


output_dir = "student_click_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


code_module = "AAA"


query = """
SELECT SV.id_student, SV.id_site, SV.sum_click, SV.date 
FROM StudentVle SV 
WHERE SV.code_module = %s
"""

vle_list = pd.read_sql_query(query, database_connection, params=(code_module,))


# Función para pivotear y exportar el dataframe
def pivot_and_export(df, student_id):
    # Asegurarse de que no hay duplicados agregando los datos por 'date' y 'id_site'
    aggregated_df = df.groupby(["date", "id_site"]).sum_click.sum().reset_index()

    # Pivotear los datos agregados
    pivot_df = aggregated_df.pivot(
        index="date", columns="id_site", values="sum_click"
    ).fillna(0)

    # Ajustar los nombres de las columnas
    pivot_df.columns = [f"id_{col}" for col in pivot_df.columns]

    # Reiniciar el índice para incluir la fecha en los datos del CSV
    pivot_df.reset_index(inplace=True)

    csv_path = os.path.join(output_dir, f"student_{student_id}_click_data.csv")
    # Exportar a CSV
    pivot_df.to_csv(csv_path, index=False)


# Iterar por cada estudiante y exportar sus datos usando la función modificada
for student_id, group in vle_list.groupby("id_student"):
    pivot_and_export(group, student_id)
