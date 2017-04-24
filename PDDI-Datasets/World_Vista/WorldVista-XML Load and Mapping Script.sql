
	--Script to Parse XML file containing All WorldVista files
	--Added 2/4/2016 By Serkan modified by Rich Boyce
	--Last Modified 2/15/2016

	--LOADs WorldVista Table data from an XML FILE
	--drop table [PDDI_Databases].[dbo].WorldVistaRawXml
	-- SELECT XmlContent
	-- INTO [PDDI_Databases].[dbo].WorldVistaRawXml
	-- FROM (SELECT *    
	--	  FROM OPENROWSET (BULK 'E:\Research\BioInformatics\Datasets\WorldVista\all_eng_tables2015-v3\all_eng_tables2015.xml', SINGLE_CLOB) 
	-- AS XmlContent) AS R(XmlContent)
	  
	--This is the Bulk imported XML in the DB table
	-- SELECT [XmlContent]  FROM [PDDI_Databases].[dbo].[WorldVistaRawXml] 
			
	-- XML Format Sample 
	--<?xml version="1.0" encoding="utf-8" ?>
	--<INTERACTIONS>
		--<INTERACTION>
			--<SOURCE>
				--<CLINICAL_SOURCE>ANSM</CLINICAL_SOURCE>
				--<SOURCE_FILE>100-BUPRENORPHINE.html
				--</SOURCE_FILE>
			--</SOURCE>
			--<DRUG1>
				--<DRUG name="BUPRENORPHINE" rxcui="1819">
				--<ATC code="N02AE01" />
				--<ATC code="N07BC01" />
				--<ATC code="N07BC51" />
				--</DRUG>
			--</DRUG1>
			--<DRUG2>
				--<CLASS name="AMPRENAVIR (AND, BY EXTRAPOLATION, FOSAMPRENAVIR)" code="J05AE0-001" />
			--</DRUG2>
			--<DESCRIPTION>Risk of increase or decrease of the effects of the buprenorphine, due to the simultaneous inhibition and acceleration of its metabolism by the protease inhibitor</DESCRIPTION>
			--<SEVERITY>Take into account</SEVERITY>
		--</INTERACTION>
	 --</INTERACTIONS>
	  
	--Extracts the Fields values in the DDIs from the document formatted like sample above
	--This Query uses XQuery to parse XML document and extract the fields in discreet form
	DECLARE @xml2 xml
	SELECT @xml2 = [XmlContent] FROM [PDDI_Databases].[dbo].WorldVistaRawXml 
	--Insert DDIs into the Table
	SELECT DISTINCT
		   dsource.scol.value('(CLINICAL_SOURCE/text())[1]', 'varchar(50)') Clinical_Source
		  ,dsource.scol.value('(SOURCE_FILE/text())[1]', 'varchar(2000)') Source_File  	
		  ,drug1.d1col.value('(DRUG/@name)[1]', 'varchar(100)') Drug1_Name 
		  ,drug1.d1col.value('(DRUG/@rxcui)[1]', 'varchar(50)')  Drug1_Rxcui   
		  ,drug1.d1col.value('(DRUG/ATC/@code)[1]', 'varchar(50)')  Drug1_ATC1 	
		  ,drug1.d1col.value('(DRUG/ATC/@code)[2]', 'varchar(50)')  Drug1_ATC2 	
		  ,drug1.d1col.value('(DRUG/ATC/@code)[3]', 'varchar(50)')  Drug1_ATC3 	
		  ,drug1.d1col.value('(DRUG/ATC/@code)[4]', 'varchar(50)')  Drug1_ATC4	
		  ,drug1.d1col.value('(CLASS/@name)[1]', 'varchar(200)')  Drug1_Class_Name
		  ,drug1.d1col.value('(CLASS/@code)[1]', 'varchar(50)')  Drug1_Class_Code
		  ,drug2.d2col.value('(DRUG/@name)[1]', 'varchar(100)')  Drug2_Name
		  ,drug2.d2col.value('(DRUG/@rxcui)[1]', 'varchar(50)') Drug2_Rxcui	
		  ,drug2.d2col.value('(DRUG/ATC/@code)[1]', 'varchar(50)') Drug2_ATC1 
		  ,drug2.d2col.value('(DRUG/ATC/@code)[2]', 'varchar(50)') Drug2_ATC2 
		  ,drug2.d2col.value('(DRUG/ATC/@code)[3]', 'varchar(50)') Drug2_ATC3 
		  ,drug2.d2col.value('(DRUG/ATC/@code)[4]', 'varchar(50)') Drug2_ATC4 	  
		  ,drug2.d2col.value('(CLASS/@name)[1]', 'varchar(200)') Drug2_Class_Name
		  ,drug2.d2col.value('(CLASS/@code)[1]', 'varchar(50)') Drug2_Class_Code 
		  ,doc.col.value('(DESCRIPTION/text())[1]', 'varchar(2000)') DDI_Description
		  ,doc.col.value('(SEVERITY/text())[1]', 'varchar(2000)') DDI_Severity
		  ,doc.col.value('(COMMENT/text())[1]', 'varchar(2000)') DDI_Comment		   
	INTO [PDDI_Databases].[dbo].WorldVista_DDIs
	FROM @xml2.nodes('/INTERACTIONS/INTERACTION') doc(col) CROSS APPLY
		  col.nodes('SOURCE') AS dsource(scol) CROSS APPLY 
		  col.nodes('DRUG1') AS drug1(d1col) CROSS APPLY
		  col.nodes('DRUG2') AS drug2(d2col)  
	    

GO   
-- (2846 row(s) affected)


-- LOADs WorldVista DDI groups data from XML
  -- SELECT GroupsXmlContent
  --	 INTO [PDDI_Databases].[dbo].WorldVistaGroupsRawXml
--	 FROM (SELECT *    
--		  FROM OPENROWSET (BULK 'E:\Dropbox\World_Vista\full-dataset-xml\all_eng_groups2015.xml', SINGLE_CLOB) 
--	     AS GroupsXmlContent) AS R(GroupsXmlContent)
	  
  --This is the Bulk imported XML in the DB table
--  SELECT [GroupsXmlContent]  FROM [PDDI_Databases].[dbo].[WorldVistaGroupsRawXml] 

---- Example data
--- <CLASSES>
---  <CLASS name="ACETYL-CHOLINESTERASE INHIBITORS" code="ACETCHO">
---   <SOURCE>
--     <CLINICAL_SOURCE>ANSM</CLINICAL_SOURCE> 
---    <SOURCE_FILE>ACETYL-CHOLINESTERASE-INHIBITORS.html</SOURCE_FILE> 
--    </SOURCE>
--    <DRUG name="Ambenonium" rxnorm="623">
--     <ATC code="N07AA30" /> 
--    </DRUG>
--    <DRUG name="Donepezil" rxnorm="135447">
--     <ATC code="N06DA02" /> 
--     <ATC code="N06DA52" /> 
--    </DRUG>
--  </CLASS>
-- </CLASSES>


    --Extracts the Fields values in the drug groups table from the document formatted like sample above
	--This Query uses XQuery to parse XML document and extract the fields in discreet form
	DECLARE @xml2 xml
	SELECT @xml2 = [GroupsXmlContent]  FROM [PDDI_Databases].[dbo].[WorldVistaGroupsRawXml] 
	--Insert data into a Table
	SELECT DISTINCT
		   doc.col.value('(SOURCE/CLINICAL_SOURCE/text())[1]', 'varchar(1000)') Clinical_Source
		  ,doc.col.value('(SOURCE/SOURCE_FILE/text())[1]', 'varchar(2000)') Source_File  
		  	
		  ,drug.dcol.value('(@name)[1]', 'varchar(100)') Drug_Name 
		  ,drug.dcol.value('(@rxnorm)[1]', 'varchar(50)')  Drug_Rxcui   
		  ,drug.dcol.value('(ATC/@code)[1]', 'varchar(50)')  Drug1_ATC1 	
		  ,drug.dcol.value('(ATC/@code)[2]', 'varchar(50)')  Drug1_ATC2 	
		  ,drug.dcol.value('(ATC/@code)[3]', 'varchar(50)')  Drug1_ATC3 	
		  ,drug.dcol.value('(ATC/@code)[4]', 'varchar(50)')  Drug1_ATC4	
		  		   
		  ,doc.col.value('(@name)[1]', 'varchar(2000)') DrugGroupName
		  ,doc.col.value('(@code)[1]', 'varchar(2000)') DrugGroupCode
	INTO [PDDI_Databases].[dbo].WorldVista_DrugGroups
	FROM @xml2.nodes('/CLASSES/CLASS') doc(col) CROSS APPLY
	     col.nodes('DRUG') AS drug(dcol) 

GO
-- (2133 row(s) affected)

/********************************************************/
-- Create a table the is the union of:
-- * all DDIs with rxcuis for d1 and d2 AND
-- * all DDIs with rxcuis for d1 and a group for d2 AND
-- * all DDIs with a group for d1 and rxcui for d2
-- * all DDIs with a group for d1 and a group for d2
/*******************************************************/ 
SELECT * INTO [PDDI_Databases].[dbo].WorldVista_RxNormCodedDDIs
FROM (
 SELECT Drug1_Name AS d1_name,
        Drug1_Rxcui AS d1_rxcui,
		Drug1_Class_Name AS d1_class_name,
		Drug1_Class_Code AS d1_class_code, 
	    Drug2_Name AS d2_name,
	    Drug2_Rxcui AS d2_rxcui,
		Drug2_Class_Code AS d2_class_code,
		Drug2_Class_Name AS d2_class_name,
		DDI_Severity,
		DDI_Description,
		DDI_Comment,
		wv_ddis.Source_File
 FROM [PDDI_Databases].[dbo].[WorldVista_DDIs] wv_ddis
 WHERE Drug1_Rxcui != ''
   AND Drug2_Rxcui != '' 
 UNION
 SELECT wv_groups.Drug_Name AS d1_name,
        wv_groups.Drug_Rxcui AS d1_rxcui,
		Drug1_Class_Name AS d1_class_name,
		Drug1_Class_Code AS d1_class_code, 
	    Drug2_Name AS d2_name,
	    Drug2_Rxcui AS d2_rxcui,
		Drug2_Class_Code AS d2_class_code,
		Drug2_Class_Name AS d2_class_name,
		DDI_Severity,
		DDI_Description,
		DDI_Comment,
		wv_ddis.Source_File
 FROM [PDDI_Databases].[dbo].[WorldVista_DDIs] wv_ddis 
  INNER JOIN WorldVista_DrugGroups wv_groups 
  ON wv_ddis.Drug1_Class_Code = wv_groups.DrugGroupCode
 WHERE wv_ddis.Drug1_Class_Code IS NOT NULL
  AND wv_ddis.Drug2_Rxcui IS NOT NULL 
  AND wv_ddis.Drug2_Rxcui != ''
  AND wv_groups.Drug_Rxcui != '' 
  AND wv_groups.Drug_Rxcui IS NOT NULL 
 UNION
 SELECT Drug1_Name AS d1_name,
	    Drug1_Rxcui AS d1_rxcui,
        Drug1_Class_Name AS d1_class_name,
		Drug1_Class_Code AS d1_class_code, 
	    wv_groups.Drug_Name AS d2_name,
        wv_groups.Drug_Rxcui AS d2_rxcui,		
		Drug2_Class_Code AS d2_class_code,
		Drug2_Class_Name AS d2_class_name,
		DDI_Severity,
		DDI_Description,
		DDI_Comment,
		wv_ddis.Source_File
 FROM [PDDI_Databases].[dbo].[WorldVista_DDIs] wv_ddis 
  INNER JOIN WorldVista_DrugGroups wv_groups 
  ON wv_ddis.Drug2_Class_Code = wv_groups.DrugGroupCode
 WHERE wv_ddis.Drug2_Class_Code IS NOT NULL
  AND wv_ddis.Drug1_Rxcui IS NOT NULL 
  AND wv_ddis.Drug1_Rxcui != ''
  AND wv_groups.Drug_Rxcui != ''
  AND wv_groups.Drug_Rxcui IS NOT NULL 
 UNION
 SELECT wv_groups1.Drug_Name AS d1_name,
        wv_groups1.Drug_Rxcui AS d1_rxcui,		
        Drug1_Class_Name AS d1_class_name,
		Drug1_Class_Code AS d1_class_code, 
	    wv_groups2.Drug_Name AS d2_name,
        wv_groups2.Drug_Rxcui AS d2_rxcui,		
		Drug2_Class_Code AS d2_class_code,
		Drug2_Class_Name AS d2_class_name,
		DDI_Severity,
		DDI_Description,
		DDI_Comment,
		wv_ddis.Source_File
 FROM [PDDI_Databases].[dbo].[WorldVista_DDIs] wv_ddis 
  INNER JOIN [PDDI_Databases].[dbo].WorldVista_DrugGroups wv_groups1 
  ON wv_ddis.Drug1_Class_Code = wv_groups1.DrugGroupCode
  INNER JOIN [PDDI_Databases].[dbo].WorldVista_DrugGroups wv_groups2
  ON wv_ddis.Drug2_Class_Code = wv_groups2.DrugGroupCode
 WHERE wv_ddis.Drug1_Class_Code IS NOT NULL
  AND wv_ddis.Drug2_Class_Code IS NOT NULL
  AND wv_groups1.Drug_Rxcui != ''
  AND wv_groups1.Drug_Rxcui IS NOT NULL
  AND wv_groups2.Drug_Rxcui != '' 
  AND wv_groups2.Drug_Rxcui IS NOT NULL
) AS tmp

GO
-- (115741 row(s) affected) 


/********************************************************/
--Get Mapping Results
/*******************************************************/ 
		 
	------------- Mappings using [INCHI_OR_Syns_OR_Name]-------------------
	--This query only retrieves the DDI pairs when both Drug1 and Drug2 can be mapped to Drugbank ID 
	--Via RXCUIs OR FDA prefered name OR INCHI_OR_Syns_OR_Name mappings OR string match OR Synonym OR Brand Names 
	IF OBJECT_ID('tempdb..#PDDIs_OR') IS NOT NULL
	BEGIN
		 DROP TABLE #PDDIs_OR
	END
	SELECT DISTINCT		 			   
			COALESCE(f1.FDA_Preferred_Term, sy1.[Synonym], br1.brand ) [Drug_1_Name],
			COALESCE(f1.drugbank_id, sy1.[drugbankid] , br1.[drugbankid] )  [Drug1_DrugbankID],
			COALESCE(f2.FDA_Preferred_Term, sy2.[Synonym], br2.brand ) [Drug_2_Name],
			COALESCE(f2.drugbank_id, sy2.[drugbankid] , br2.[drugbankid])[Drug2_DrugbankID],
			DDI_Severity,
			Source_File,
			DDI_Description, 
			DDI_Comment
	INTO #PDDIs_OR 		 
	FROM [PDDI_Databases].[dbo].WorldVista_RxNormCodedDDIs b 
			LEFT JOIN [PDDI_Databases].[dbo].[FDA_RXNORM_DRUGBANK] r1 ON r1.[RxNorm_CUI] = b.d1_rxcui  
			LEFT JOIN [PDDI_Databases].[dbo].[FDA_RXNORM_DRUGBANK] r2 ON r2.[RxNorm_CUI] = b.d2_rxcui  
			LEFT JOIN [PDDI_Databases].[dbo].[INCHI_OR_Syns_OR_Name] f1 ON f1.[FDA_preferred_term] = b.d1_name 
																			OR f1.[DrugBank_name] = b.d1_name 
			LEFT JOIN [PDDI_Databases].[dbo].[INCHI_OR_Syns_OR_Name] f2 ON f2.[FDA_preferred_term] = b.d2_name
																			OR f2.[DrugBank_name] = b.d2_name 
			LEFT JOIN (Select d.drugbankid, d.[Synonym] 
					   From [PDDI_Databases].[dbo].[DrugbankSynonyms] d
							LEFT JOIN [PDDI_Databases].[dbo].[MultipleSynonyms] m ON m.Common_Synonym = d.[Synonym]
						Where Common_Synonym IS NULL
					   ) sy1 ON sy1.[Synonym]= b.d1_name 
			LEFT JOIN (Select d.drugbankid, d.[Synonym] 
					   From [PDDI_Databases].[dbo].[DrugbankSynonyms] d
							LEFT JOIN [PDDI_Databases].[dbo].[MultipleSynonyms] m ON m.Common_Synonym = d.[Synonym]
						Where Common_Synonym IS NULL
					   ) sy2 ON sy2.[Synonym]= b.d2_name
			LEFT JOIN (Select d.drugbankid, d.brand 
					   From [PDDI_Databases].[dbo].[DrugbankBrands] d
							LEFT JOIN [PDDI_Databases].[dbo].[MultipleBrandNames] m ON m.Common_BrandName = d.brand
						Where Common_BrandName IS NULL
					   ) br1 ON br1.brand= b.d1_name
			LEFT JOIN (Select d.drugbankid, d.brand 
					   From [PDDI_Databases].[dbo].[DrugbankBrands] d
							LEFT JOIN [PDDI_Databases].[dbo].[MultipleBrandNames] m ON m.Common_BrandName = d.brand
						Where Common_BrandName IS NULL
					   ) br2 ON br2.brand= b.d2_name
	WHERE  (r1.DrugBank_CUI IS NOT NULL OR f1.drugbank_id IS NOT NULL OR sy1.drugbankid IS NOT NULL OR br1.drugbankid IS NOT NULL)
			 AND (r2.DrugBank_CUI IS NOT NULL OR f2.drugbank_id IS NOT NULL OR sy2.drugbankid IS NOT NULL OR br2.drugbankid IS NOT NULL)  
GO	
--(51870 row(s) affected)

	-- We have to replace newlines with HTML break tags because of examples like the following
	-- SELECT REPLACE(DDI_Description, char(10),'<BR>') FROM WorldVista_RxNormCodedDDIs WHERE d1_rxcui = '3098' AND d2_rxcui = '25287' 
	
	--Get PDDIs Mapped to Drugbank - 44785 PDDIs
	SELECT DISTINCT		 
			  ISNULL([Drug_1_Name],'')    
			+'$'+ ISNULL([Drug1_DrugbankID],'')   
			+'$'+ ISNULL([Drug_2_Name],'')   
			+'$'+ ISNULL([Drug2_DrugbankID],'')    
			+'$'+ ISNULL(DDI_Severity,'') 
			+'$'+ REPLACE(ISNULL(Source_File,''), CHAR(10), '')
			+'$'+ REPLACE(ISNULL(DDI_Description,''), CHAR(10), '<BR>')
			+'$'+ REPLACE(ISNULL(DDI_Comment,''), CHAR(10), '<BR>') 
			+'$' 		
	FROM #PDDIs_OR b 
	WHERE [Drug1_DrugbankID] IS NOT NULL AND [Drug2_DrugbankID]IS NOT NULL
	  


	------------- Mappings using [INCHI_AND_Syns_OR_Name]-------------------	
	--This part of the script is the same as above except it uses INCHI_AND_Syns_OR_Name Mapping instead of INCHI_OR_Syns_OR_Name
	IF OBJECT_ID('tempdb..#PDDIs_AND') IS NOT NULL
	BEGIN
		 DROP TABLE #PDDIs_AND
	END
	SELECT DISTINCT		 			   
			COALESCE(f1.FDA_Preferred_Term, sy1.[Synonym], br1.brand ) [Drug_1_Name],
			COALESCE(f1.drugbank_id, sy1.[drugbankid] , br1.[drugbankid] )  [Drug1_DrugbankID],
			COALESCE(f2.FDA_Preferred_Term, sy2.[Synonym], br2.brand ) [Drug_2_Name],
			COALESCE(f2.drugbank_id, sy2.[drugbankid] , br2.[drugbankid])[Drug2_DrugbankID],
			DDI_Severity,
			Source_File,
			DDI_Description, 
			DDI_Comment
	INTO #PDDIs_AND 		
	FROM [PDDI_Databases].[dbo].WorldVista_RxNormCodedDDIs b 
			LEFT JOIN [PDDI_Databases].[dbo].[FDA_RXNORM_DRUGBANK] r1 ON r1.[RxNorm_CUI]  = b.d1_rxcui  
			LEFT JOIN [PDDI_Databases].[dbo].[FDA_RXNORM_DRUGBANK] r2 ON r2.[RxNorm_CUI] = b.d2_rxcui	
			LEFT JOIN [PDDI_Databases].[dbo].[INCHI_AND_Syns_OR_Name] f1 ON f1.[FDA_preferred_term] = b.d1_name 
																			OR f1.[DrugBank_name] = b.d1_name 
			LEFT JOIN [PDDI_Databases].[dbo].[INCHI_AND_Syns_OR_Name] f2 ON f2.[FDA_preferred_term] = b.d2_name
																			OR f2.[DrugBank_name] = b.d2_name
			LEFT JOIN (Select d.drugbankid, d.[Synonym] 
					   From [PDDI_Databases].[dbo].[DrugbankSynonyms] d
							LEFT JOIN [PDDI_Databases].[dbo].[MultipleSynonyms] m ON m.Common_Synonym = d.[Synonym]
						Where Common_Synonym IS NULL
					   ) sy1 ON sy1.[Synonym]= b.d1_name 
			LEFT JOIN (Select d.drugbankid, d.[Synonym] 
					   From [PDDI_Databases].[dbo].[DrugbankSynonyms] d
							LEFT JOIN [PDDI_Databases].[dbo].[MultipleSynonyms] m ON m.Common_Synonym = d.[Synonym]
						Where Common_Synonym IS NULL
					   ) sy2 ON sy2.[Synonym]= b.d2_name
			LEFT JOIN (Select d.drugbankid, d.brand 
					   From [PDDI_Databases].[dbo].[DrugbankBrands] d
							LEFT JOIN [PDDI_Databases].[dbo].[MultipleBrandNames] m ON m.Common_BrandName = d.brand
						Where Common_BrandName IS NULL
					   ) br1 ON br1.brand= b.d1_name
			LEFT JOIN (Select d.drugbankid, d.brand 
					   From [PDDI_Databases].[dbo].[DrugbankBrands] d
							LEFT JOIN [PDDI_Databases].[dbo].[MultipleBrandNames] m ON m.Common_BrandName = d.brand
						Where Common_BrandName IS NULL
					   ) br2 ON br2.brand= b.d2_name
	WHERE  (f1.drugbank_id IS NOT NULL OR sy1.drugbankid IS NOT NULL OR br1.drugbankid IS NOT NULL)
			 AND (f2.drugbank_id IS NOT NULL OR sy2.drugbankid IS NOT NULL OR br2.drugbankid IS NOT NULL)  
		 
	--(21156 row(s) affected)


	--Get PDDIs Mapped to Drugbank - 21156 PDDIs
	SELECT DISTINCT		 
			  ISNULL([Drug_1_Name],'')    
			+'$'+ ISNULL([Drug1_DrugbankID],'')   
			+'$'+ ISNULL([Drug_2_Name],'')   
			+'$'+ ISNULL([Drug2_DrugbankID],'')    
			+'$'+ ISNULL(DDI_Severity,'') 
			+'$'+ REPLACE(ISNULL(Source_File,''), CHAR(10), '')
			+'$'+ REPLACE(ISNULL(DDI_Description,''), CHAR(10), '<BR>')
			+'$'+ REPLACE(ISNULL(DDI_Comment,''), CHAR(10), '<BR>')
			+'$' 		
	FROM #PDDIs_AND b 
	WHERE [Drug1_DrugbankID] IS NOT NULL AND [Drug2_DrugbankID]IS NOT NULL
	 
 
	 
 
