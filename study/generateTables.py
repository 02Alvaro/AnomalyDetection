import os

import pandas as pd

# Ruta base de los archivos
base_path = 'anomalyDetection/metrics/'

# Leer el archivo 'all_grouped.csv'
df = pd.read_csv(os.path.join(base_path, 'all_grouped.csv'))

# Renombrar las columnas 'code_module' a 'module' y 'anomaly_rate' a 'anomalyRate'
df.rename(columns={'code_module': 'module', 'anomaly_rate': 'anomalyRate'}, inplace=True)

# Seleccionar las métricas a procesar
metrics = ['se', 'sp', 'p', 'roc']

# Diccionario de algoritmos y sus parámetros correspondientes
algorithms = {
    "knn": "n_neighbors",
    "lof": "n_neighbors",
    "cof": "n_neighbors",
    "cblof": "n_clusters",
    "hbos": "n_bins",
    "autoencoder": "latent_size",
    "dae": "latent_size",
}

# Diccionario de valores de parámetros para cada tipo
param_values = {
    "n_neighbors": [5, 10, 20, 30, 40],
    "n_clusters": [6,7,8,9,10],
    "n_bins": [5, 10, 15, 20, 25],
    "latent_size": [16, 32, 64, 128, 256]
}

# Procesar y crear archivos para cada métrica y tipo de parámetro
for metric in metrics:
    for param, values in param_values.items():
        combined_df = pd.DataFrame()

        for value in values:
            result_df = pd.DataFrame()

            for algorithm, algorithm_param in algorithms.items():
                if algorithm_param == param:
                    # Filtrar el DataFrame por algoritmo y valor de parámetro
                    df_filtered = df[(df['algorithm'] == algorithm) & (df['value'] == value)]
                    if not df_filtered.empty:
                        # Crear un nuevo DataFrame para la métrica actual
                        metric_mean = df_filtered.pivot_table(values=f'{metric}_mean', index=['module', 'value', 'type', 'samples', 'dims', 'anomalyRate'], columns='algorithm')
                        metric_std = df_filtered.pivot_table(values=f'{metric}_std', index=['module', 'value', 'type', 'samples', 'dims', 'anomalyRate'], columns='algorithm')

                        temp_df = metric_mean.astype(str) + " ± " + metric_std.astype(str)
                        temp_df.columns = [f"{algorithm}" for algorithm in temp_df.columns]

                        if result_df.empty:
                            result_df = temp_df
                        else:
                            result_df = result_df.join(temp_df, how='outer')

            # Añadir los resultados del valor actual al DataFrame combinado
            if combined_df.empty:
                combined_df = result_df.reset_index()
            else:
                combined_df = pd.concat([combined_df, result_df.reset_index()])

        # Ordenar por 'type', 'module', 'value'
        combined_df = combined_df.sort_values(by=['type', 'module', 'value'])

        # Crear el nombre del archivo
        file_name = f'{metric}_metrics_{param}.csv'
        
        # Guardar el DataFrame en un archivo CSV
        combined_df.to_csv(os.path.join(base_path, file_name), index=False)

        # separamos por modulo y se agrega e
        for module, group in combined_df.groupby('module'):
            if not os.path.exists(os.path.join(base_path,"module_division")):
                os.makedirs(os.path.join(base_path,"module_division"))
            if not os.path.exists(os.path.join(base_path,"module_division",module)):
                os.makedirs(os.path.join(base_path,"module_division",module))
            group.to_csv(os.path.join(base_path,"module_division",module,f'{metric}_metrics_{param}_{module}.csv'), index=False)
    
print("Archivos combinados generados con éxito.")
