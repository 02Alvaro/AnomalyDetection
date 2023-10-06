#required having user and password in ~/.my.cnf
curso="AAA"
studentIndex=65002

if [ $# -eq 2 ]; then
  curso=$1
  studentIndex=$2
else
  echo "curso AAA y studentIndex 65002 por defecto"
fi

queryStudentInfo="
USE OpenUniversityData;
SELECT 
  S.id_student,
  S.code_module,
  S.code_presentation,
  S.num_of_prev_attempts,
  S.studied_credits,
  S.final_result,
  SR.date_registration,
  SR.date_unregistration
  FROM 
      StudentInfo S, StudentRegistration SR 
  WHERE
      S.code_module= SR.code_module and 
      S.code_presentation=SR.code_presentation and 
      S.id_student=SR.id_student and
      S.code_module = '$curso' AND S.id_student = '$studentIndex';"

queryAssessments="
USE OpenUniversityData;
SELECT
    SA.id_assessment,
  IFNULL(SA.date_submitted, -1),
  IFNULL(SA.score, -1)
FROM 
    StudentAssessment SA, Assessments A
WHERE
    SA.id_student = '$studentIndex' and SA.id_assessment=A.id_assessment and A.code_module='$curso'
ORDER BY
    SA.id_assessment;"

queryVle="
USE OpenUniversityData;
SELECT 
    SV.id_site,
  sum(SV.sum_click) AS total_clicks
FROM 
    StudentVle SV , Vle V
WHERE
    SV.id_student = '$studentIndex' and SV.id_site=V.id_site and V.code_module='$curso'
group by SV.id_site
ORDER BY
    SV.id_site;"

mysql -e "$queryStudentInfo"
mysql -e "$queryAssessments"
mysql -e "$queryVle"
