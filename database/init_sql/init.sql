USE OpenUniversityData;

CREATE TABLE
    Courses (
        code_module VARCHAR(3) NOT NULL,
        code_presentation VARCHAR(5) NOT NULL,
        length INT (3),
        PRIMARY KEY (code_module, code_presentation)
    );

CREATE TABLE
    Assessments (
        code_module VARCHAR(3) NOT NULL,
        code_presentation VARCHAR(5) NOT NULL,
        id_assessment INT (5),
        assessment_type VARCHAR(4),
        date INT(3) NULL,
        weight FLOAT (3),
        PRIMARY KEY (id_assessment),
        FOREIGN KEY (code_module, code_presentation) REFERENCES Courses (code_module, code_presentation)
    );

CREATE TABLE
    Vle (
        id_site INT (7),
        code_module VARCHAR(3) NOT NULL,
        code_presentation VARCHAR(5) NOT NULL,
        activity_type VARCHAR(45),
        week_from INT (2) NULL,
        week_to INT (2) NULL,
        PRIMARY KEY (id_site),
        FOREIGN KEY (code_module, code_presentation) REFERENCES Courses (code_module, code_presentation)
    );

CREATE TABLE
    StudentInfo (
        code_module VARCHAR(3) NOT NULL,
        code_presentation VARCHAR(5) NOT NULL,
        id_student INT (8),
        gender VARCHAR(1),
        region VARCHAR(255),
        highest_education VARCHAR(255),
        imd_band VARCHAR(255),
        age_band VARCHAR(255),
        num_of_prev_attempts INT (3),
        studied_credits INT (4),
        disability VARCHAR(10),
        final_result VARCHAR(255),
        PRIMARY KEY (id_student, code_module, code_presentation),
        FOREIGN KEY (code_module, code_presentation) REFERENCES Courses (code_module, code_presentation)
    );

CREATE TABLE
    StudentRegistration (
        code_module VARCHAR(3) NOT NULL,
        code_presentation VARCHAR(5) NOT NULL,
        id_student INT (8),
        date_registration INT,
        date_unregistration INT,
        FOREIGN KEY (id_student, code_module, code_presentation) REFERENCES StudentInfo (id_student, code_module, code_presentation)
    );

CREATE TABLE
    StudentAssessment (
        id_assessment INT,
        id_student INT,
        date_submitted INT,
        is_banked INT,
        score INT NULL,
        PRIMARY KEY (id_assessment, id_student),
        FOREIGN KEY (id_assessment) REFERENCES Assessments (id_assessment),
        FOREIGN KEY (id_student) REFERENCES StudentInfo (id_student)
    );

CREATE TABLE
    StudentVle (
        code_module VARCHAR(3) NOT NULL,
        code_presentation VARCHAR(5) NOT NULL,
        id_student INT,
        id_site INT,
        date INT NULL,
        sum_click INT,
        FOREIGN KEY (id_student) REFERENCES StudentInfo (id_student),
        FOREIGN KEY (id_site) REFERENCES Vle (id_site),
        FOREIGN KEY (code_module, code_presentation) REFERENCES Courses (code_module, code_presentation)
    );

LOAD DATA infile '/var/lib/mysql-files/init_csv/courses.csv' INTO TABLE Courses FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;

LOAD DATA infile '/var/lib/mysql-files/init_csv/assessments.csv' INTO TABLE Assessments FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS (code_module,code_presentation,id_assessment,assessment_type,@var_date,weight)
SET date = NULLIF(@var_date, '');

LOAD DATA infile '/var/lib/mysql-files/init_csv/vle.csv' INTO TABLE Vle FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS (id_site,code_module,code_presentation,activity_type,@var_week_from,@var_week_to)
SET week_from = NULLIF(@var_week_from, ''),week_to = NULLIF(@var_week_to, '');

LOAD DATA infile '/var/lib/mysql-files/init_csv/studentInfo.csv' INTO TABLE StudentInfo FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;

LOAD DATA infile '/var/lib/mysql-files/init_csv/studentRegistration.csv' INTO TABLE StudentRegistration FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS (code_module,code_presentation,id_student,@var_date_registration,@var_date_unregistration)
SET date_unregistration = NULLIF(@var_date_unregistration, ''),date_registration = NULLIF(@var_date_registration, '');

LOAD DATA infile '/var/lib/mysql-files/init_csv/studentAssessment.csv' INTO TABLE StudentAssessment FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS (id_assessment, id_student, date_submitted, is_banked, @var_score)
SET score = NULLIF(@var_score, '');

LOAD DATA infile '/var/lib/mysql-files/init_csv/studentVle.csv' INTO TABLE StudentVle FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;
