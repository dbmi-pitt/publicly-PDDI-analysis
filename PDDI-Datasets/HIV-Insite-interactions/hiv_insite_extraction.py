# hiv_insite_extraction.py
# Read .html files in folder:
#   HIV-Insite-interactions
# Retrieve 2 drug names, quality of evidence, summary, and description of ddi
# Consolidate all such DDI's from each folder as .tsv file

import glob
import os
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup

################### GLOBAL VARIABLES ###################

DEBUG = True

# INPUT FILE FOLDERS
HEP_DDI_PATH = "../HEP-drug-interactions"
HIV_DDI_PATH = "../HIV-drug-interactions"
HIV_INSITE_DDI_PATH = "../HIV-Insite-interactions"

# OUTPUT FILES
HEP_OUTFILE_NAME = "HEP-drug-interactions.tsv"
HIV_OUTFILE_NAME = "HIV-drug-interactions.tsv"
HIV_INSITE_OUTFILE_NAME = "HIV-Insite-interactions.tsv"

########################################################

outfile = codecs.open(HIV_INSITE_OUTFILE_NAME, encoding='utf-8', mode='w+')
outfile.write(u"Drug 1 Name\tDrug 2 Name\tSummary\tDescription\n")

os.chdir(HIV_INSITE_DDI_PATH)
for file in glob.glob("*.html"):
    if DEBUG:
        print(file)
    f = codecs.open(file, encoding='utf-8', mode='r+')
    soup = BeautifulSoup(f, "html.parser")
    f.close()
outfile.close()
