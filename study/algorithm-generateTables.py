import os

import pandas as pd

# Ruta base de los archivos
base_path = 'anomalyDetection/metrics/'
dir_path = 'algorithm_comparison'

# Leer el archivo 'all_grouped.csv'
df = pd.read_csv(os.path.join(base_path, 'all_grouped.csv'))

# Renombrar columnas
df.rename(columns={'code_module': 'module', 'anomaly_rate': 'anomalyRate'}, inplace=True)

# Función para combinar media y desviación estándar
def combine_mean_std(row, col_base):
    mean = row[f"{col_base}_mean"]
    std = row[f"{col_base}_std"]
    return f"{mean}±{std}"

# Aplicar la función a las columnas correspondientes
columns_to_combine = ['se', 'sp', 'p', 'roc']
for col in columns_to_combine:
    df[col] = df.apply(lambda row: combine_mean_std(row, col), axis=1)
    df.drop([f"{col}_mean", f"{col}_std"], axis=1, inplace=True)

# Crear directorio si no existe
os.makedirs(os.path.join(base_path, dir_path), exist_ok=True)

# Agrupar por 'module' y 'algorithm' y guardar en archivos separados
grouped = df.groupby(['module', 'algorithm'])
for (module, algorithm), group in grouped:
    module_dir = os.path.join(base_path, dir_path, module)
    os.makedirs(module_dir, exist_ok=True)
    
    # Crear el nombre del archivo
    file_name = f'{module}_{algorithm}.csv'
    
    # Eliminar la columna 'algorithm' y 'module' antes de guardar
    group = group.drop(['algorithm', 'module'], axis=1)

    # Ordena por value,type
    group = group.sort_values(by=[ 'type','value'])


    # Guardar el DataFrame correspondiente en un archivo CSV
    group.to_csv(os.path.join(module_dir, file_name), index=False)
