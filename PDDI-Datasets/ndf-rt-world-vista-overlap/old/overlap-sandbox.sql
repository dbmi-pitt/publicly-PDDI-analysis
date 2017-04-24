# 269527 in NDF-RT
SELECT count(drug_interaction_id) FROM ndf_rt_interaction;
SELECT * FROM ndf_rt_interaction;
SELECT * FROM ndf_rt_interaction WHERE drug_1_rxcui = 3008 AND drug_2_rxcui = 10594;
SELECT * FROM ndf_rt_interaction WHERE drug_1_rxcui = 1005921 AND drug_2_rxcui = 4103;

# 2846 interactions in World Vista
SELECT count(drug_interaction_id) FROM drug_interaction;
SELECT * FROM drug_interaction;
SELECT * FROM drug_interaction WHERE drug_1_rxcui = 3008 AND drug_2_rxcui = 10594;
SELECT * FROM drug_interaction WHERE drug_1_rxcui = 1005921 AND drug_2_rxcui = 4103;
# RxCui's 3008 and 10594 are one example that should overlap

SELECT w.drug_1_rxcui AS world_vista_drug_1,
       w.drug_2_rxcui AS world_vista_drug_2,
       n.drug_1_rxcui AS ndf_rt_drug_1,
       n.drug_2_rxcui AS ndf_rt_drug_2
FROM drug_interaction w
INNER JOIN ndf_rt_interaction n
ON (w.drug_1_rxcui = n.drug_1_rxcui AND w.drug_2_rxcui = n.drug_2_rxcui);
/*WHERE w.drug_1_rxcui = 3008
AND n.drug_1_rxcui = 3008
AND w.drug_2_rxcui = 10594
AND n.drug_2_rxcui = 10594;*/

SELECT w.Drug_1_RxCUI AS world_vista_drug_1,
       w.Drug_2_RxCUI AS world_vista_drug_2,
       n.drug_1_rxcui AS ndf_rt_drug_1,
       n.drug_2_rxcui AS ndf_rt_drug_2
FROM drug_interaction w
INNER JOIN NDF_RT_INTERACTION n
ON (w.Drug_1_RxCUI = n.drug_1_rxcui AND w.dDrug_2_RxCUI = n.drug_2_rxcui);
-- 581 in this overlap (no class overlap)
-- 269527 interactions in NDF-RT
-- 137821 interactions in World Vista when all permutations of class code drugs are accounted for

SELECT g.Drug_Name AS Drug_1_Name,
       g.RxNorm AS Drug_1_RxNorm,
       g.Class_Code AS Class_Code_1,
       h.Drug_Name AS Drug_2_Name,
       h.RxNorm AS Drug_2_RxNorm,
       h.Class_Code AS Class_Code_2,
       i.*
FROM drug_interaction i
LEFT JOIN drug_group g
ON (i.Drug_1_Code = TRIM(TRAILING '\r' FROM g.Class_Code))
LEFT JOIN drug_group h
ON (i.Drug_2_Code = TRIM(TRAILING '\r' FROM h.Class_Code))
ORDER BY i.Drug_Interaction_ID asc;

###############################################################################################################

# 265435 rows cumulative from both data sets (when no blanks, no nulls, duplicates permitted via UNION ALL).
# 261303 rows when no duplicates via UNION
# difference = 5715
# TODO: 1007804, 1111, more have some drug_2_rxcui new line characters
SELECT w.drug_1_rxcui, w.drug_2_rxcui 
FROM drug_interaction w
WHERE w.drug_1_rxcui is not null AND w.drug_2_rxcui is not null
UNION ALL
SELECT n.drug_1_rxcui, n.drug_2_rxcui
FROM ndf_rt_interaction n
WHERE n.drug_1_rxcui is not null AND n.drug_2_rxcui is not null;

# 4577 rows returned for interactions that are in both data sets in any capacity.
SELECT u.drug_1_rxcui, u.drug_2_rxcui, COUNT(*)
FROM(
	SELECT w.drug_1_rxcui, w.drug_2_rxcui 
	FROM drug_interaction w
	WHERE w.drug_1_rxcui is not null AND w.drug_2_rxcui is not null
	UNION ALL
	SELECT n.drug_1_rxcui, n.drug_2_rxcui
	FROM ndf_rt_interaction n
	WHERE n.drug_1_rxcui is not null AND n.drug_2_rxcui is not null) u
GROUP BY u.drug_1_rxcui, u.drug_2_rxcui
HAVING COUNT(*) > 1;

###############################################################################################################

# Original query, but would not fetch

SELECT *
FROM drug_class_interaction w
INNER JOIN NDF_RT_INTERACTION n
ON ((w.Drug_1_RxCUI = n.drug_1_rxcui AND w.Drug_2_RxCUI = n.drug_2_rxcui)
	OR (w.Drug_1_RxNorm = n.drug_1_rxcui AND w.Drug_2_RxCUI = n.drug_2_rxcui)
	OR (w.Drug_1_RxCUI = n.drug_1_rxcui AND w.Drug_2_RxNorm = n.drug_2_rxcui)
    OR (w.Drug_1_RxNorm = n.drug_1_rxcui AND w.Drug_2_RxNorm = n.drug_2_rxcui));
    
###############################################################################################################

/* 269527 total PDDI's in NDF-RT
264135 PDDI's in NDF-RT where the RxCUI mapping is not null. For the overlap analysis, the RxCUI entry must not be null.
137821 PDDI's in WorldVista when permutations of drugs in drug classes are accounted for.
391668 cumulatively with duplicates and no null entries.
354305 with no duplicates and no null entries. */

SELECT drug_1_rxcui AS rxcui_1, 
		   drug_1_rxcui AS rxnorm_1, 
		   drug_2_rxcui AS rxcui_2, 
		   drug_2_rxcui AS rxnorm_2
	FROM NDF_RT_INTERACTION
	WHERE drug_1_rxcui is not null
    AND drug_2_rxcui is not null
	UNION ALL
	SELECT Drug_1_RxCUI, Drug_1_RxNorm, Drug_2_RxCUI, Drug_2_RxNorm
	FROM Drug_Class_Interaction
    WHERE (Drug_1_RxCUI is not null
    OR Drug_1_RxNorm is not null)
    AND (Drug_2_RxCUI is not null 
    OR Drug_2_RxNorm is not null);

# 67 pddis in NDF-RT where both rxcuis are the same

SELECT * FROM ndf_rt_interaction WHERE drug_1_rxcui = drug_2_rxcui;

# 240 pddis in overlap where both are the same
    
SELECT * FROM (SELECT * FROM (
	SELECT drug_1_rxcui AS rxcui_1, 
		   drug_1_rxcui AS rxnorm_1, 
		   drug_2_rxcui AS rxcui_2, 
		   drug_2_rxcui AS rxnorm_2
	FROM NDF_RT_INTERACTION
	WHERE drug_1_rxcui is not null
    AND drug_2_rxcui is not null
	UNION ALL
	SELECT Drug_1_RxCUI, Drug_1_RxNorm, Drug_2_RxCUI, Drug_2_RxNorm
	FROM Drug_Class_Interaction
    WHERE (Drug_1_RxCUI is not null
    OR Drug_1_RxNorm is not null)
    AND (Drug_2_RxCUI is not null 
    OR Drug_2_RxNorm is not null)
) AS all_pddi 
GROUP BY rxcui_1, rxnorm_1, rxcui_2, rxnorm_2
HAVING COUNT(*) > 1) AS p
WHERE (rxcui_1 = rxnorm_2
OR rxnorm_1 = rxnorm_2
OR rxnorm_1 = rxcui_2
OR (rxcui_1 = rxcui_2 
AND rxcui_1 is not null
AND rxcui_2 is not null));

# 26893

SELECT * FROM (
	SELECT drug_1_rxcui AS rxcui_1, 
		   drug_1_rxcui AS rxnorm_1, 
		   drug_2_rxcui AS rxcui_2, 
		   drug_2_rxcui AS rxnorm_2
	FROM NDF_RT_INTERACTION
	WHERE drug_1_rxcui is not null
	AND drug_2_rxcui is not null
	UNION ALL
	SELECT Drug_1_RxCUI, Drug_1_RxNorm, Drug_2_RxCUI, Drug_2_RxNorm
	FROM Drug_Class_Interaction
	WHERE (Drug_1_RxCUI is not null
	OR Drug_1_RxNorm is not null)
	AND (Drug_2_RxCUI is not null
	OR Drug_2_RxNorm is not null)
) AS all_pddi 
GROUP BY rxcui_1, rxnorm_1, rxcui_2, rxnorm_2
HAVING COUNT(*) > 1;

# 26653 = 26893 - 240 where the singular RxCUI above are removed

CREATE VIEW Drug_Class_Interaction_View AS (
SELECT i.Drug_Interaction_ID,
	   i.Drug_1_Name,
       i.Drug_1_RxCUI,
       g.RxNorm AS Drug_1_RxNorm,
       i.Drug_1_Class_Name,
       i.Drug_1_Code,
       i.Drug_2_Name,
       i.Drug_2_RxCUI,
       h.RxNorm AS Drug_2_RxNorm,
       i.Drug_2_Class_Name,
       i.Drug_2_Code,
	   g.Drug_Name AS Drug_Name_1,
       g.Class_Code AS Class_Code_1,
       h.Drug_Name AS Drug_Name_2,
       h.Class_Code AS Class_Code_2
FROM Drug_Interaction i
LEFT JOIN Drug_Group g
ON (i.Drug_1_Code = TRIM(TRAILING '\r' FROM g.Class_Code))
LEFT JOIN Drug_Group h
ON (i.Drug_2_Code = TRIM(TRAILING '\r' FROM h.Class_Code)));

SELECT * FROM(
	SELECT * FROM (
		SELECT drug_1_rxcui AS rxcui_1, 
			   drug_1_rxcui AS rxnorm_1, 
			   drug_2_rxcui AS rxcui_2, 
			   drug_2_rxcui AS rxnorm_2
		FROM NDF_RT_INTERACTION
		WHERE drug_1_rxcui is not null
		AND drug_2_rxcui is not null
		UNION ALL
		SELECT Drug_1_RxCUI, Drug_1_RxNorm, Drug_2_RxCUI, Drug_2_RxNorm
		FROM Drug_Class_Interaction_View
		WHERE (Drug_1_RxCUI is not null
		OR Drug_1_RxNorm is not null)
		AND (Drug_2_RxCUI is not null
		OR Drug_2_RxNorm is not null)
	) AS all_pddi 
	GROUP BY rxcui_1, rxnorm_1, rxcui_2, rxnorm_2
	HAVING COUNT(*) > 1) as overlap_pddi
WHERE ((rxnorm_1 != rxnorm_2) OR (rxnorm_1 is null OR rxnorm_2 is null)) AND
	  ((rxcui_1 != rxnorm_2) OR (rxcui_1 is null OR rxnorm_2 is null)) AND
      ((rxnorm_1 != rxcui_2) OR (rxnorm_1 is null OR rxcui_2 is null)) AND
      ((rxcui_1 != rxcui_2) OR (rxcui_1 is null OR rxcui_2 is null));
