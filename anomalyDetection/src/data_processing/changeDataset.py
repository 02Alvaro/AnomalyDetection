import os
import pandas as pd

datasets = ["AAA.csv","BBB.csv","CCC.csv","DDD.csv"]
output_directory = '../TimeEval-algorithms-main/1-data/'
for dataset in datasets:

    df = pd.read_csv(os.path.join(os.getcwd(), 'coursesData', dataset))

    df.drop(['code_module', 'code_presentation', 'id_student'], axis=1, inplace=True)

    df['is_anomaly'] = df['final_result'].replace({
        'Fail': 0,
        'Withdrawn': 1,
        'Pass': 0,
        'Distinction': 0
    })
    df.drop('final_result', axis=1, inplace=True)

    df.reset_index(inplace=True)
    df.rename(columns={'index': 'timestamp'}, inplace=True)

    filename = os.path.join(output_directory, f'Processed_{dataset}')
    df.to_csv(filename, index=False)