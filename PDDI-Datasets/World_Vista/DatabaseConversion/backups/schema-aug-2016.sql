DROP TABLE IF EXISTS Drug_Interaction CASCADE;
DROP TABLE IF EXISTS ATC_Code CASCADE;
DROP TABLE IF EXISTS Drug_Group CASCADE;

CREATE TABLE Drug_Group (
	Drug_Name varchar(250) NOT NULL,
	RxNorm varchar(50),
	Source_File INT NOT NULL,
	Clinical_Source varchar(50) NOT NULL,
	Class_Name varchar(250) NOT NULL,
	Class_Code varchar(50) NOT NULL,
	PRIMARY KEY (Drug_Name, Source_File, Class_Name)
) ENGINE=INNODB DEFAULT CHARSET=utf8;

CREATE TABLE ATC_Code (
	ATC_Code varchar(20) NOT NULL,
	Drug_Name varchar(250) NOT NULL,
	PRIMARY KEY (ATC_Code, Drug_Name)
) ENGINE=INNODB DEFAULT CHARSET=utf8;

CREATE TABLE Drug_Interaction (
	Drug_Interaction_ID INT NOT NULL,
	Drug_1_Name varchar(250),
	Drug_1_RxCUI varchar(50),
	Drug_1_Class_Name varchar(250),
	Drug_1_Code varchar(50),
	Drug_2_Name varchar(250),
	Drug_2_RxCUI varchar(50),
	Drug_2_Class_Name varchar(250),
	Drug_2_Code varchar(50),
	Clinical_Source varchar(50) NOT NULL,
	Source_File varchar(100) NOT NULL,
	Description varchar(2000),
	Severity varchar(500),
	`Comment` varchar(3000),
	PRIMARY KEY (Drug_Interaction_ID)
) ENGINE=INNODB DEFAULT CHARSET=utf8;

LOAD DATA LOCAL INFILE './eng_groups2016_xml.tsv' INTO TABLE Drug_Group FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' IGNORE 1 LINES (Drug_Name, RxNorm, Source_File, Clinical_Source, Class_Name, Class_Code);

LOAD DATA LOCAL INFILE './eng_groups_tables_2016_xml_atc_codes.tsv' INTO TABLE ATC_Code FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' IGNORE 1 LINES (ATC_Code, Drug_Name);

LOAD DATA LOCAL INFILE './eng_tables2016-xml.tsv' INTO TABLE Drug_Interaction FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' IGNORE 1 LINES (Drug_Interaction_ID, Drug_1_Name, Drug_1_RxCUI, Drug_1_Class_Name, Drug_1_Code, Drug_2_Name, Drug_2_RxCUI, Drug_2_Class_Name, Drug_2_Code, Clinical_Source, Source_File, Description, Severity, `Comment`);

SET SQL_SAFE_UPDATES=0;

UPDATE Drug_Interaction
SET Drug_1_RxCUI = NULL
WHERE Drug_1_RxCUI = '';

UPDATE Drug_Interaction
SET Drug_2_RxCUI = NULL
WHERE Drug_2_RxCUI = '';

UPDATE Drug_Group
SET RxNorm  = NULL
WHERE RxNorm = '';