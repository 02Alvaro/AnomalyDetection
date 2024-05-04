import os

import pandas as pd


def check_anomaly_proportions(output_dir, fold_count=5):
    # Cargar el dataset completo para comprobar su proporción de anomalías
    full_data_path = os.path.join(output_dir, "all_students_click_data_activity_type.csv")
    full_df = pd.read_csv(full_data_path)
    full_anomaly_ratio = full_df['is_anomaly'].mean() * 100
    print(f"Total dataset anomaly ratio: {full_anomaly_ratio:.2f}%\n")

    anomaly_ratios = [{'type': 'full_dataset', 'anomaly_ratio': full_anomaly_ratio}]

    for i in range(1, fold_count + 1):
        train_path = os.path.join(output_dir, f"train_fold_{i}.csv")
        test_path = os.path.join(output_dir, f"test_fold_{i}.csv")

        # Cargar datos de entrenamiento y prueba
        train_df = pd.read_csv(train_path)
        test_df = pd.read_csv(test_path)

        # Calcular el porcentaje de anomalías
        train_anomaly_ratio = train_df['is_anomaly'].mean() * 100
        test_anomaly_ratio = test_df['is_anomaly'].mean() * 100

        # Guardar y mostrar los resultados
        anomaly_ratios.append({
            'fold': i,
            'train_anomaly_ratio': train_anomaly_ratio,
            'test_anomaly_ratio': test_anomaly_ratio
        })
        print(f"Fold {i}:")
        print(f"  Training set anomaly ratio: {train_anomaly_ratio:.2f}%")
        print(f"  Testing set anomaly ratio: {test_anomaly_ratio:.2f}%\n")

    return anomaly_ratios

if __name__ == "__main__":
    output_dir = "activityTypeDataset2"  # Asegúrate de que este es el directorio correcto
    print("Comprobando las proporciones de anomalías en el conjunto completo y cada fold...")
    check_anomaly_proportions(output_dir)
