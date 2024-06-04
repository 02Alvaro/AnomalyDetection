import os
import re

import pandas as pd

# Lista de archivos
files = [
    'cblofallReports.csv',
    'cofallReports.csv',
    'hbosallReports.csv',
    'knnallReports.csv',
    'lofallReports.csv'
]

# Ruta base de los archivos
base_path = 'anomalyDetection/metrics/'

# Función para modificar el nombre del modelo
def modify_model_name(model_name):
    #modified_name = re.sub(r'_fold_\d+_seed_\d+', '', model_name)
    modified_name = re.sub(r'_activity_type_clicks_sum_\w+_fold_\d+_seed_\d+_\d+.pkl', '', model_name)
    return modified_name

# Lista para almacenar los DataFrames procesados
processed_dfs = []

# Procesar cada archivo
for file in files:
    csv_file = os.path.join(base_path, file)
    
    # Leer el archivo CSV
    df = pd.read_csv(csv_file)

    # Aplicar la modificación al nombre del modelo
    df['model'] = df['model'].apply(modify_model_name)

    # Seleccionar solo las columnas numéricas para el cálculo de medias
    numeric_columns = df.select_dtypes(include='number').columns

    # Agregar la columna 'model' para agrupar
    columns_to_group = ['model'] + list(numeric_columns)

    # Agrupar por el nombre del modelo modificado y calcular las medias
    grouped_df = df[columns_to_group].groupby('model').mean().reset_index()

    # Añadir el DataFrame procesado a la lista
    processed_dfs.append(grouped_df)

# Concatenar todos los DataFrames procesados
final_df = pd.concat(processed_dfs)

# Guardar el resultado en un nuevo archivo CSV
output_file = os.path.join(base_path, 'combined_reports.csv')
final_df.to_csv(output_file, index=False)

# Mostrar el DataFrame resultante (opcional)
print("Resultado final combinado:")
print(final_df)

print("Todos los archivos han sido procesados y combinados en un solo fichero.")
