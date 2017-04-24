DROP TABLE IF EXISTS Drug_Class_Interaction;

# Temporary table to include different drugs belonging to drug groups in the drug interaction table
CREATE TABLE Drug_Class_Interaction AS (
SELECT i.Drug_Interaction_ID,
	   i.Drug_1_Name,
       COALESCE(i.Drug_1_RxCUI,g.RxNorm) AS drug_1_rxcui,
       i.Drug_1_Class_Name,
       i.Drug_1_Code,
       i.Drug_2_Name,
       COALESCE(i.Drug_2_RxCUI,h.RxNorm) AS drug_2_rxcui,
       i.Drug_2_Class_Name,
       i.Drug_2_Code,
	   g.Drug_Name AS Drug_Name_1,
       i.Drug_1_RxCUI AS Drug_1_RxNorm,
       g.RxNorm AS Drug_1_RxNorm_Group,
       g.Class_Code AS Class_Code_1,
       h.Drug_Name AS Drug_Name_2,
       i.Drug_2_RxCUI AS Drug_2_RxNorm,
       h.RxNorm AS Drug_2_RxNorm_Group,
       h.Class_Code AS Class_Code_2
FROM Drug_Interaction i
LEFT JOIN Drug_Group g
ON (i.Drug_1_Code = TRIM(TRAILING '\r' FROM g.Class_Code))
LEFT JOIN Drug_Group h
ON (i.Drug_2_Code = TRIM(TRAILING '\r' FROM h.Class_Code))
WHERE COALESCE(i.Drug_1_RxCUI,g.RxNorm) != COALESCE(i.Drug_2_RxCUI,h.RxNorm)
GROUP BY COALESCE(i.Drug_1_RxCUI,g.RxNorm), COALESCE(i.Drug_2_RxCUI,h.RxNorm));

# Remove reverse duplicates (ex. pairs where [drug a, drug b] and [drug b, drug a] are in the table)
# Index to improve performance
CREATE INDEX wv_index ON Drug_Class_Interaction(drug_1_rxcui, drug_2_rxcui);

DELETE a
FROM Drug_Class_Interaction a
INNER JOIN Drug_Class_Interaction b
ON b.drug_2_rxcui = a.drug_1_rxcui
AND b.drug_1_rxcui = a.drug_2_rxcui
WHERE a.drug_1_rxcui > a.drug_2_rxcui;

# Intersect of WorldVista and NDF-RT datasets

SELECT rx1.STR, drug_1_rxcui, rx2.STR, drug_2_rxcui FROM(
	SELECT * FROM (
		SELECT drug_1_rxcui,
			   drug_2_rxcui
		FROM NDF_RT_INTERACTION
		WHERE drug_1_rxcui is not null
		AND drug_2_rxcui is not null
		GROUP BY drug_1_rxcui, drug_2_rxcui
		UNION ALL
		SELECT drug_1_rxcui, drug_2_rxcui
		FROM Drug_Class_Interaction
		WHERE drug_1_rxcui is not null 
		AND drug_2_rxcui is not null
	) AS all_pddi 
	WHERE drug_1_rxcui != drug_2_rxcui 
	GROUP BY drug_1_rxcui, drug_2_rxcui
	HAVING COUNT(*) > 1) AS overlap
INNER JOIN rxnorm.RXNCONSO AS rx1 ON drug_1_rxcui = rx1.RXCUI
INNER JOIN rxnorm.RXNCONSO AS rx2 ON drug_2_rxcui = rx2.RXCUI
GROUP BY drug_1_rxcui, drug_2_rxcui
INTO OUTFILE 'worldvista-NDFRT-overlap.csv'
FIELDS ENCLOSED BY '"'
TERMINATED BY ','
LINES TERMINATED BY '\n';

# Set difference of PDDI's that are only in the NDF-RT data set.

SELECT rx1.STR, d.drug_1_rxcui, rx2.STR, d.drug_2_rxcui FROM(
	SELECT n.drug_1_rxcui, n.drug_2_rxcui FROM NDF_RT_INTERACTION n
	LEFT JOIN(
		SELECT * FROM (
			SELECT drug_1_rxcui,
				   drug_2_rxcui
			FROM NDF_RT_INTERACTION
			WHERE drug_1_rxcui is not null
			AND drug_2_rxcui is not null
			GROUP BY drug_1_rxcui, drug_2_rxcui
			UNION ALL
			SELECT drug_1_rxcui, drug_2_rxcui
			FROM Drug_Class_Interaction
			WHERE drug_1_rxcui is not null 
			AND drug_2_rxcui is not null
		) AS all_pddi 
		WHERE drug_1_rxcui != drug_2_rxcui 
		GROUP BY drug_1_rxcui, drug_2_rxcui
		HAVING COUNT(*) > 1
	) o 
	ON o.drug_1_rxcui = n.drug_1_rxcui
	AND o.drug_2_rxcui = n.drug_2_rxcui
	WHERE o.drug_1_rxcui is null
	AND o.drug_2_rxcui is null
	AND n.drug_1_rxcui is not null
	AND n.drug_2_rxcui is not null
	GROUP BY n.drug_1_rxcui, n.drug_2_rxcui) AS d
INNER JOIN rxnorm.RXNCONSO AS rx1 ON d.drug_1_rxcui = rx1.RXCUI
INNER JOIN rxnorm.RXNCONSO AS rx2 ON d.drug_2_rxcui = rx2.RXCUI
GROUP BY d.drug_1_rxcui, d.drug_2_rxcui
INTO OUTFILE 'NDFRT-set-difference.csv'
FIELDS ENCLOSED BY '"'
TERMINATED BY ','
LINES TERMINATED BY '\n';

# Set difference of PDDI's that are only in the WorldVista data set.

SELECT rx1.STR, d.drug_1_rxcui, rx2.STR, d.drug_2_rxcui FROM(
	SELECT w.drug_1_rxcui, w.drug_2_rxcui FROM Drug_Class_Interaction w
	LEFT JOIN(
		SELECT * FROM (
			SELECT drug_1_rxcui,
				   drug_2_rxcui
			FROM NDF_RT_INTERACTION
			WHERE drug_1_rxcui is not null
			AND drug_2_rxcui is not null
			GROUP BY drug_1_rxcui, drug_2_rxcui
			UNION ALL
			SELECT drug_1_rxcui, drug_2_rxcui
			FROM Drug_Class_Interaction
			WHERE drug_1_rxcui is not null 
			AND drug_2_rxcui is not null
		) AS all_pddi 
		WHERE drug_1_rxcui != drug_2_rxcui 
		GROUP BY drug_1_rxcui, drug_2_rxcui
		HAVING COUNT(*) > 1
	) o 
	ON o.drug_1_rxcui = w.drug_1_rxcui
	AND o.drug_2_rxcui = w.drug_2_rxcui
	WHERE o.drug_1_rxcui is null
	AND o.drug_2_rxcui is null
	AND w.drug_1_rxcui is not null
	AND w.drug_2_rxcui is not null
	GROUP BY w.drug_1_rxcui, w.drug_2_rxcui) AS d
LEFT JOIN rxnorm.RXNCONSO AS rx1 ON d.drug_1_rxcui = rx1.RXCUI
LEFT JOIN rxnorm.RXNCONSO AS rx2 ON d.drug_2_rxcui = rx2.RXCUI
GROUP BY d.drug_1_rxcui, d.drug_2_rxcui
INTO OUTFILE 'worldvista-set-difference.csv'
FIELDS ENCLOSED BY '"'
TERMINATED BY ','
LINES TERMINATED BY '\n';
