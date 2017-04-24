import os, codecs
import sys
import xml.etree.ElementTree as ET

GROUP_FOLDER_PATH = "./eng_groups_sept2016-xml"
GROUP_OUTFILE_NAME = "eng_groups2016_xml-v3.tsv"

TABLES_FOLDER_PATH = "./eng_tables_sept2016-xml"
TABLES_OUTFILE_NAME = "eng_tables2016-xml-v3.tsv"

GROUPS_ATC_CODES_OUTFILE = "eng_groups_tables_2016_xml_atc_codes-v2.tsv"

##### GROUPS #####
groups_outfile = codecs.open(GROUP_OUTFILE_NAME, 'w', 'utf-8')

groups_outfile.write(u"Drug Name\tRxNorm\tSource File\tClinical Source\tClass Name\tClass Code\n")
atc_dict = {}

for fp in os.listdir(GROUP_FOLDER_PATH):  
  if fp.endswith(".xml"):
    fp_full = os.path.join(GROUP_FOLDER_PATH, fp)
    print "Processing " + fp_full
    with open(fp_full) as f:
      tree = ET.parse(f)
      root = tree.getroot()
      print('root')
      print root
      for k in root.getchildren():
        print('1')
        print k
        # CLASS
        if(k.tag == 'CLASS'):
          class_name = k.get('name').strip()
          class_code = k.get('code').strip()

        for i in k.getchildren():
          print('2')
          print i
          # SOURCE
          for j in i.getchildren():
            print j
            if(j.tag == 'CLINICAL_SOURCE'):
              clinical_source = j.text
            if(j.tag == 'SOURCE_FILE'):
              source_file = j.text

          # DRUG
          if(i.tag == 'DRUG'):
            drug_name = i.get('name')
            rxnorm = i.get('rxnorm')

            if rxnorm is None:
              rxnorm = ''
            print(u"%s\t%s\t%s\t%s\t%s\t%s\n" % ((drug_name.upper()).rstrip('\n'), rxnorm.rstrip('\n'), source_file.rstrip('\n'), clinical_source.rstrip('\n'), class_name.rstrip('\n'), class_code.rstrip('\n')) )
            groups_outfile.write(u"%s\t%s\t%s\t%s\t%s\t%s\n" % ((drug_name.upper()).rstrip('\n'), rxnorm.rstrip('\n'), source_file.rstrip('\n'), clinical_source.rstrip('\n'), class_name.rstrip('\n'), class_code.rstrip('\n')) )

            for j in i.getchildren():
              if(j.tag == 'ATC'):
                atc_code = j.get('code').strip()
                atc_dict[atc_code.strip().rstrip('\n') + "\t" + drug_name.upper()] = ""

groups_outfile.close()

### TABLES #####
tables_outfile = codecs.open(TABLES_OUTFILE_NAME, 'w', 'utf-8')

tables_outfile.write(u"Drug Interaction ID\tDrug 1 Name\tDrug 1 RxCUI\tDrug 1 Class Name\tDrug 1 Code\tDrug 2 Name\tDrug 2 RxCUI\tDrug 2 Class Name\tDrug 2 Code\tClinical Source\tSource File\tDescription\tSeverity\tComment\n")

drug_interaction_id = 0
drug_codes = {}
drug_code_id = 0
drug_class_codes = {}
drug_class_code_id = 0
general_drug_id = 0
drug_interaction_id = 0

for fp in os.listdir(TABLES_FOLDER_PATH):
  if fp.endswith(".xml"):
    fp_full = os.path.join(TABLES_FOLDER_PATH, fp)
    print "Processing " + fp_full
    with open(fp_full) as f:
      tree = ET.parse(f)
      root = tree.getroot()
      
      for i in root.getchildren():
        if(i.tag == 'INTERACTION'):
          comment = ''
          drug_1_name = ''
          drug_1_rxcui = ''
          drug_1_class_name = ''
          drug_1_code = ''
          drug_2_name = ''
          drug_2_rxcui = ''
          drug_2_class_name = ''
          drug_2_code = ''
          description = ''
          severity = ''
          source_file = ''
          clinical_source = ''

          for j in i.getchildren():
            
            # SOURCE
            if(j.tag == 'SOURCE'):
              for k in j.getchildren():
                if(k.tag == 'CLINICAL_SOURCE'):
                  clinical_source = k.text.strip()
                if(k.tag == 'SOURCE_FILE'):
                  source_file = k.text.strip()

            # DRUG1
            if(j.tag == 'DRUG1'):
              for k in j.getchildren():
                if(k.tag == 'DRUG'):
                  drug_1_name = k.get('name')
                  drug_1_rxcui = k.get('rxcui')

                  for l in k.getchildren():
                    if(l.tag == 'ATC'):
                      atc_dict[l.get('code').strip().rstrip('\n') + "\t" + drug_1_name.upper().strip().rstrip('\n')] = ""

                if(k.tag == 'CLASS'):
                  drug_1_class_name = k.get('name').strip()
                  drug_1_code = k.get('code').strip()

            # DRUG2
            if(j.tag == 'DRUG2'):
              for k in j.getchildren():
                if(k.tag == 'DRUG'):
                  drug_2_name = k.get('name')
                  drug_2_rxcui = k.get('rxcui')

                  for l in k.getchildren():
                    if(l.tag == 'ATC'):
                      atc_dict[l.get('code').strip().rstrip('\n') + "\t" + drug_2_name.upper().strip().rstrip('\n')] = ""

                if(k.tag == 'CLASS'):
                  drug_2_class_name = k.get('name')
                  drug_2_code = k.get('code')
                  
            # DESCRIPTION
            if(j.tag == 'DESCRIPTION'):
              description = j.text

            # SEVERITY
            if(j.tag == 'SEVERITY'):
              severity = j.text

            # COMMENT
            if(j.tag == 'COMMENT'):
              comment = j.text

          if comment is None:
            comment = ''
          if description is None:
            description = ''
          if severity is None:
            severity = ''
          if source_file is None:
            source_file = ''
          if clinical_source is None:
            clinical_source = ''
          if drug_1_name is None:
            drug_1_name = ''
          if drug_1_rxcui is None:
            drug_1_rxcui = ''
          if drug_1_class_name is None:
            drug_1_class_name = ''
          if drug_1_code is None:
            drug_1_code = ''
          if drug_2_name is None:
            drug_2_name = ''
          if drug_2_rxcui is None:
            drug_2_rxcui = ''
          if drug_2_class_name is None:
            drug_2_class_name = ''
          if drug_2_code is None:
            drug_2_code = ''

          tables_outfile.write(u"%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % ( (str(drug_interaction_id)).strip().rstrip('\n'), (drug_1_name.upper()).strip().rstrip('\n'), drug_1_rxcui.strip().rstrip('\n'), drug_1_class_name.strip().rstrip('\n'), drug_1_code.strip().rstrip('\n'), (drug_2_name.upper()).strip().rstrip('\n'), drug_2_rxcui.strip().rstrip('\n'), drug_2_class_name.strip().rstrip('\n'), drug_2_code.strip().rstrip('\n'), clinical_source.strip().rstrip('\n'), source_file.strip().rstrip('\n'), description.strip().rstrip('\n').replace('\n', ''), severity.strip().rstrip('\n'), comment.strip().rstrip('\n')))
          drug_interaction_id += 1

tables_outfile.close()

### ATC CODES ###
atc_codes_outfile = codecs.open(GROUPS_ATC_CODES_OUTFILE, 'w', 'utf-8')
atc_codes_outfile.write(u"ATC Code\tDrug Name\n")

for key, value in atc_dict.items():
  atc_codes_outfile.write(u"%s\n" % ( key.strip().rstrip(' \t\n\r') ) )

atc_codes_outfile.close()

sys.exit(0)
