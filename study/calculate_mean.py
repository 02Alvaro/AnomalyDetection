import os
import re

import pandas as pd

# Ruta base de los archivos
base_path = 'anomalyDetection/metrics/'

# Lista de archivos
files = [
    'cblofallReports.csv',
    'cofallReports.csv',
    'hbosallReports.csv',
    'knnallReports.csv',
    'lofallReports.csv',
    'autoencoderallReports.csv',
    'daeallReports.csv',
]

# Expresión regular para extraer la información del modelo
pattern = re.compile(r'(?P<algorithm>\w+)_(?P<folder>activity_type_clicks_sum)_(?P<code_module>\w+)_fold_(?P<fold>\d+)_seed_(?P<seed>\d+)_(?P<value>\d+)\.pkl')

# Función para procesar cada archivo
def process_file(file):
    # Leer el archivo CSV
    df = pd.read_csv(os.path.join(base_path, file))
    
    # Inicializar nuevas columnas
    df['algorithm_parsed'] = ''
    df['folder_parsed'] = ''
    df['code_module_parsed'] = ''
    df['fold_parsed'] = ''
    df['seed_parsed'] = ''
    df['value_parsed'] = ''
    df['type'] = ''
    
    # Extraer y asignar la información a las nuevas columnas
    for index, row in df.iterrows():
        match = pattern.match(row['model'])
        if match:
            df.at[index, 'algorithm_parsed'] = match.group('algorithm')
            df.at[index, 'folder_parsed'] = match.group('folder')
            df.at[index, 'code_module_parsed'] = match.group('code_module')
            df.at[index, 'fold_parsed'] = match.group('fold')
            df.at[index, 'seed_parsed'] = match.group('seed')
            df.at[index, 'value_parsed'] = match.group('value')
        # Determinar el tipo (train o test) basado en el dataset
        if 'train' in row['dataset']:
            df.at[index, 'type'] = 'train'
        elif 'test' in row['dataset']:
            df.at[index, 'type'] = 'test'
    
    return df

def group_and_calculate(df):    
    # Agrupar por las columnas especificadas y calcular la media y la desviación estándar
    grouped_df = df.groupby(['algorithm_parsed', 'code_module_parsed', 'value_parsed', 'type']).agg({
        'samples': ['mean'],
        'dims': ['mean'],
        'anomaly_rate': ['mean'],
        'se': ['mean', 'std'],
        'sp': ['mean', 'std'],
        'p': ['mean', 'std'],
        'roc': ['mean', 'std'],
    }).reset_index()

    grouped_df = grouped_df.round(4)

    # Renombrar las columnas
    grouped_df.columns = ['algorithm', 'code_module', 'value', 'type', 'samples', 'dims', 'anomaly_rate', 'se_mean', 'se_std', 'sp_mean', 'sp_std', 'p_mean', 'p_std', 'roc_mean', 'roc_std']
    
    return grouped_df

# Inicializar una lista para almacenar todos los DataFrames agrupados
all_grouped_dfs = []

# Procesar cada archivo en la lista
for file in files:
    df = process_file(file)
    grouped_df = group_and_calculate(df)
    all_grouped_dfs.append(grouped_df)

# Concatenar todos los DataFrames agrupados
final_df = pd.concat(all_grouped_dfs, ignore_index=True)

# Guardar el DataFrame final en un archivo CSV
final_df.to_csv(os.path.join(base_path, 'all_grouped.csv'), index=False)

print("Procesamiento y guardado final completado.")
