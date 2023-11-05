import pandas as pd
from sqlalchemy import create_engine

database_username = "root"
database_password = "anomaly"
database_ip = "db"
database_name = "OpenUniversityData"

database_connection = create_engine(
    "mysql+pymysql://{0}:{1}@{2}/{3}".format(
        database_username, database_password, database_ip, database_name
    )
)

for code_module in ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG"]:
    student_list = pd.read_sql_query(
        "SELECT id_student,code_module,code_presentation,num_of_prev_attempts,studied_credits,final_result FROM StudentInfo WHERE code_module = %s order by id_student",
        database_connection,
        params=[code_module],
    )
    vle_list = pd.read_sql_query(
        "SELECT SV.id_student, SV.id_site, sum(SV.sum_click) as sum_click FROM StudentVle SV,Vle V WHERE  SV.id_site=V.id_site and V.code_module = %s GROUP BY SV.id_student, SV.id_site ORDER BY SV.id_student, SV.id_site",
        database_connection,
        params=[code_module],
    )
    assessment_list = pd.read_sql_query(
        "SELECT SA.id_student, SA.id_assessment,IFNULL(SA.date_submitted, -1) as date_submitted,IFNULL(SA.score, -1) as score FROM StudentAssessment SA, Assessments A WHERE A.id_assessment= SA.id_assessment and A.code_module = %s order by SA.id_student, SA.id_assessment",
        database_connection,
        params=[code_module],
    )

    # Pivot and merge the dataframes
    assessment_list = assessment_list.pivot_table(
        index="id_student", columns="id_assessment"
    ).reset_index()
    assessment_list.columns = ["id_student"] + [
        f"{col[0]}{col[1]}" for col in assessment_list.columns[1:]
    ]

    vle_list = vle_list.pivot_table(
        index="id_student", columns="id_site", values="sum_click"
    ).reset_index()
    vle_list.columns = ["id_student"] + [f"clicks_{i}" for i in vle_list.columns[1:]]

    # Now let's merge all the information into the student_list DataFrame
    df = pd.merge(student_list, assessment_list, on="id_student", how="left")
    df = pd.merge(df, vle_list, on="id_student", how="left")

    # Fill NaN values with -1 (or whatever value you want to use to represent 'no data')
    df.fillna(-1, inplace=True)
    filename = f"{code_module}.csv"
    df.to_csv(filename, index=False)
