# hiv-extraction.py
# Read .html files in folder:
#   HIV-drug-interactions
# Retrieve 2 drug names, quality of evidence, summary, and description of ddi
# Consolidate all such DDI's from each folder as .tsv file

import glob
import os
import codecs
import sys
import csv
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup

################### GLOBAL VARIABLES ###################

DEBUG = True

DRUGBANK = "drugbank.csv"

# OUTPUT FILES
HEP_OUTFILE_NAME = "HEP-drug-interactions.tsv"
HIV_OUTFILE_NAME = "HIV-drug-interactions.tsv"
HIV_INSITE_OUTFILE_NAME = "HIV-Insite-interactions.tsv"

UNMAPPED_HIV_DRUGS = "HIV-drugs-unmapped.txt"
UNMAPPED_HEP_DRUGS = "HEP-drugs-unmapped.txt"

########################################################

drugbank = csv.reader(open(DRUGBANK, mode='r'))
drug_dict = dict((rows[0], rows[1]) for rows in drugbank)

outfile = codecs.open(HIV_OUTFILE_NAME, encoding='utf-8', mode='w+')
outfile.write(u"Drug 1 Name\tDrug 1 DrugBank\tDrug 2 Name\tDrug 2 DrugBank\tQuality of Evidence\tSummary\tDescription\n")

unmapped_drugs = codecs.open(UNMAPPED_HIV_DRUGS, mode='w')
unmapped = []

for file in glob.glob("*.html"):
    if DEBUG:
        print(file)
    f = codecs.open(file, encoding='utf-8', mode='r+')
    soup = BeautifulSoup(f, "html.parser")
    ddi_list = soup.findAll('div', attrs={'class': 'interaction-block interaction-list'})
    # Each "interaction-block interaction-list" includes:
    # 2 drug names: <div class="interaction-block-inner">
    # Quality of evidence: <p><strong>Quality of Evidence:</strong>Very Low</p>
    #       <p class="interaction-block-header *">
    #       * can be:
    #           "interaction-block-header orange"
    #           "interaction-block-header green"
    #           "interaction-block-header gray outline"
    #           "interaction-block-header green outline"
    #           "interaction-block-header red"
    #           "interaction-block-header gray"
    # Summary: <strong>Summary:</strong> <div class="interaction-info-divide">
    # Description: <strong>Description:</strong> <div class="interaction-info-divide">
    for ddi in ddi_list:
        s = BeautifulSoup(str(ddi), "html.parser")
        drugs = s.findAll('div', attrs={'class': 'interaction-block-inner'})
        # quality = s.findAll('p', attrs={'class': ''})
        info = s.findAll('div', attrs={'class': 'interaction-info-block'})
        for node in drugs:
            if DEBUG:
                print node
            drug = u''.join(node.findAll(text=True)).strip()  # .decode('utf-8').replace(u"\xa0", " ").encode('utf-8')
            drug1 = drug.split(u"\n")[0]
            drugbank1 = drug_dict.get(drug1.upper(), "")
            if drugbank1 == "" and "(" in drug1:
                d1 = drug1.split("(")[0].strip()
                drugbank1 = drug_dict.get(d1.upper(), "")
            drug2 = drug.split(u"\n")[1]
            drugbank2 = drug_dict.get(drug2.upper(), "")
            if drugbank2 == "" and "(" in drug2:
                d2 = drug2.split("(")[0].strip()
                drugbank2 = drug_dict.get(d2.upper(), "")
            if DEBUG:
                # print(drug)
                print(drug1)
                print(drugbank1)
                print(drug2)
                print(drugbank2)
                if drugbank1 == "" and drug1 not in unmapped:
                    unmapped.append(drug1)
                if drugbank2 == "" and drug2 not in unmapped:
                    unmapped.append(drug2)
        # for node in quality:
        #     if DEBUG:
        #         print node
        #     q = u''.join(node.findAll(text=True)).strip()
        #     quality = q.split(u"\n")[1].strip()
        #     if DEBUG:
        #         print(q)
        #         print(quality)
        for node in info:
            if DEBUG:
                print node
            i = u''.join(node.findAll(text=True)).strip()  # .decode('utf-8').replace(u"\xa0", " ").encode('utf-8')
            # not every node has quality of evidence
            li = i.split(u"\n")
            if li[0] == 'Quality of Evidence:':
                quality = li[0]
                qualityText = li[1].strip()
                summary = li[5]
                summaryText = li[7]
                description = li[12]
                # description text can go to other <p></p> spans
                descriptionText = u''.join(li[14:])
            else:
                quality = ""
                qualityText = ""
                summary = li[0]
                summaryText = li[2]
                description = li[7]
                descriptionText = u''.join(li[9:])
            if DEBUG:
                print(i)
                print(quality)
                print(qualityText)
                print(summary)
                print(summaryText)
                print(description)
                print(descriptionText)
        # TODO quality of evidence after drug2
        outfile.write(u"%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (drug1.rstrip(u"\n"), drugbank1, drug2.rstrip(u"\n"), drugbank2, qualityText.rstrip(u"\n"), summaryText.rstrip(u"\n"), descriptionText.rstrip(u"\n")))
    f.close()
outfile.close()
unmapped_drugs.write('\n'.join(unmapped))
unmapped_drugs.close()
