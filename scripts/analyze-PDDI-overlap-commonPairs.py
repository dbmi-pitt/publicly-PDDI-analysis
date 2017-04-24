#
# analyze-PDDI-overlap-commonpairs.py
#
# Analyze the overlap potential drug-drug interactions common between sources 
#
# Authors: Serkan Ayvaz 
#
# October 2014
# 

import pickle
import json
import urllib2
import urllib
import traceback
import pickle
import sys
sys.path = sys.path + ['.']

from PDDI_Model import getPDDIDict

# See PDDI_Model for the structure of the PDDI dictionaries being parsed
DIKB_OBSERVED_PDDI_FILE = "../pickle-data/dikb-observed-ddis.pickle"
DIKB_PREDICTED_PDDI_FILE = "../pickle-data/dikb-predicted-ddis.pickle"
TWOSIDES_PDDI_FILE = "../pickle-data/twosides-ddis.pickle"
DRUGBANK_PDDI_FILE = "../pickle-data/drugbank4-ddis.pickle"
NDFRT_PDDI_FILE_INCHI_AND = "../pickle-data/ndfrt-mapped-ddis-inchi-and.pickle"
NDFRT_PDDI_FILE_INCHI_OR = "../pickle-data/ndfrt-mapped-ddis-inchi-or.pickle"
KEGG_PDDI_FILE = "../pickle-data/kegg-ddis.pickle"
CREDIBLEMEDS_PDDI_FILE = "../pickle-data/crediblemeds-ddis.pickle"
WORLDVISTA_PDDI_FILE_INCHI_AND = "../pickle-data/worldvista-ddis-inchi-and.pickle"
WORLDVISTA_PDDI_FILE_INCHI_OR = "../pickle-data/worldvista-ddis-inchi-or.pickle"
DDICORPUS2011_PDDI_FILE_INCHI_AND = "../pickle-data/ddicorpus2011-ddis-inchi-and.pickle"
DDICORPUS2011_PDDI_FILE_INCHI_OR = "../pickle-data/ddicorpus2011-ddis-inchi-or.pickle"
DDICORPUS2013_PDDI_FILE_INCHI_AND = "../pickle-data/ddicorpus2013-ddis-inchi-and.pickle"
DDICORPUS2013_PDDI_FILE_INCHI_OR = "../pickle-data/ddicorpus2013-ddis-inchi-or.pickle"
NLMCORPUS_PDDI_FILE_INCHI_AND = "../pickle-data/nlmcorpus-ddis-inchi-and.pickle"
NLMCORPUS_PDDI_FILE_INCHI_OR = "../pickle-data/nlmcorpus-ddis-inchi-or.pickle"
PKCORPUS_PDDI_FILE_INCHI_AND = "../pickle-data/pkcorpus-ddis-inchi-and.pickle"
PKCORPUS_PDDI_FILE_INCHI_OR= "../pickle-data/pkcorpus-ddis-inchi-or.pickle"
ONCHIGHPRIORITY_PDDI_FILE = "../pickle-data/onchighpriority-ddis.pickle"
ONCNONINTERUPTIVE_PDDI_FILE = "../pickle-data/oncnoninteruptive-ddis.pickle"
OSCAR_PDDI_FILE = "../pickle-data/oscar-ddis.pickle"
SEMMEDDB_PDDI_FILE = "../pickle-data/semmeddb-ddis.pickle"  

############################################################
# Utility functions
############################################################

def mapDrugPairs(l):
    """ map drug pairs to PDDI dicts. Each key points to a list of PDDIs that share a drug pair """
    d = {}
       
    for pddi in l:
         p1=pddi["drug1"]
         p2=pddi["drug2"]
         k1 = "%s-%s" % (p1, p2)
         k2 = "%s-%s" % (p2, p1)
         
         if not d.has_key(k1) and not d.has_key(k2):
             d[k1] = [pddi]
       
         if d.has_key(k1):
            d[k1].append(pddi)
            
         if d.has_key(k2):
            d[k2].append(pddi)  
                          
    return d
    
def loadPickle(FILE_Name):
     f = open(FILE_Name, 'r')
     pickle_file = pickle.load(f)
     f.close()    
     
     return pickle_file
            
def writeCommonPDDIs(fname,commonL):
    f = open(fname, "w")
    s = "drug pairs \n" 
 
    for key,val in commonL.iteritems():
        s += "%s    %s\n" % (key,val)                                          
        
    f.write(s)
    f.close()


def findOverlapTwoSets(d1, d2):
    """ Comparison is made on the drug pair, not the anticipated event"""
    common = {}
    s = ""
 
    for key,pddiL in d1.iteritems():
        k1 = "%s-%s" % (pddiL[0]["drug1"], pddiL[0]["drug2"])        
        k2 = "%s-%s" % (pddiL[0]["drug2"], pddiL[0]["drug1"])          
                                  
        if d2.has_key(k1):    
                      s= "%s\t%s\t%s"% (
                               "object:%s precipitant: %s "%(pddiL[0].get("object") ,pddiL[0].get("precipitant"))
                              ,"%s Evidence: %s "%(pddiL[0].get("source") ,pddiL[0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d2[k1][0].get("source") ,d2[k1][0].get("evidenceStatement"))
                              )
                      #print s     
                      common[k1] =s  
                          
        if d2.has_key(k2):       
                      s= "%s\t%s\t%s" % (
                               "object:%s precipitant: %s "%(pddiL[0].get("object") ,pddiL[0].get("precipitant"))
                              ,"%s Evidence: %s "%(pddiL[0].get("source") ,pddiL[0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d2[k2][0].get("source") ,d2[k2][0].get("evidenceStatement"))
                              )
                      #print s
                      common[k2] =s
#       
    return (common)


def findOverlapThreeSets(d1, d2, d3):
    """ Comparison is made on the drug pair, not the anticipated event"""
    common = {}
    s = ""
 
    for key,pddiL in d1.iteritems():
        k1 = "%s-%s" % (pddiL[0]["drug1"], pddiL[0]["drug2"])        
        k2 = "%s-%s" % (pddiL[0]["drug2"], pddiL[0]["drug1"])          
                                  
        if d2.has_key(k1):  
            if d3.has_key(k1):     
                      s= "%s\t%s\t%s\t%s"% (
                               "object:%s precipitant: %s "%(pddiL[0].get("object") ,pddiL[0].get("precipitant"))
                              ,"%s Evidence: %s "%(pddiL[0].get("source") ,pddiL[0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d2[k1][0].get("source") ,d2[k1][0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d3[k1][0].get("source") ,d3[k1][0].get("evidenceStatement"))
                              )
                      #print s     
                      common[k1] =s  
                          
        if d2.has_key(k2):  
            if d3.has_key(k2):     
                      s= "%s\t%s\t%s\t%s" % (
                               "object:%s precipitant: %s "%(pddiL[0].get("object") ,pddiL[0].get("precipitant"))
                              ,"%s Evidence: %s "%(pddiL[0].get("source") ,pddiL[0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d2[k2][0].get("source") ,d2[k2][0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d3[k2][0].get("source") ,d3[k2][0].get("evidenceStatement"))
                              )
                      #print s
                      common[k2] =s
#       
    return (common)

def findOverlapFourSets(d1, d2, d3,d4):
    """ Comparison is made on the drug pair, not the anticipated event"""
    common = {}
    s = ""
 
    for key,pddiL in d1.iteritems():
        k1 = "%s-%s" % (pddiL[0]["drug1"], pddiL[0]["drug2"])        
        k2 = "%s-%s" % (pddiL[0]["drug2"], pddiL[0]["drug1"])          
                                
        if d2.has_key(k1):  
            if d3.has_key(k1):    
                if d4.has_key(k1):    
                      s= "%s\t%s\t%s\t%s\t%s"% (
                               "object:%s precipitant: %s "%(pddiL[0].get("object") ,pddiL[0].get("precipitant"))
                              ,"%s Evidence: %s "%(pddiL[0].get("source") ,pddiL[0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d2[k1][0].get("source") ,d2[k1][0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d3[k1][0].get("source") ,d3[k1][0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d4[k1][0].get("source") ,d4[k1][0].get("evidenceStatement"))
                               )
                      #print s     
                      common[k1] =s  
                          
        if d2.has_key(k2):  
            if d3.has_key(k2): 
                if d4.has_key(k2):     
                      s= "%s\t%s\t%s\t%s\t%s" % (
                               "object:%s precipitant: %s "%(pddiL[0].get("object") ,pddiL[0].get("precipitant"))
                              ,"%s Evidence: %s "%(pddiL[0].get("source") ,pddiL[0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d2[k2][0].get("source") ,d2[k2][0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d3[k2][0].get("source") ,d3[k2][0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d4[k2][0].get("source") ,d4[k2][0].get("evidenceStatement"))
                              )
                      #print s
                      common[k2] =s
#       
    return (common)
 
def findOverlapFiveSets(d1, d2, d3, d4, d5):
    """ Comparison is made on the drug pair, not the anticipated event"""
    common = {}
    s = ""
 
    for key,pddiL in d1.iteritems():
        k1 = "%s-%s" % (pddiL[0]["drug1"], pddiL[0]["drug2"])        
        k2 = "%s-%s" % (pddiL[0]["drug2"], pddiL[0]["drug1"])          
                                
        if d2.has_key(k1):  
            if d3.has_key(k1):    
                if d4.has_key(k1): 
                    if d5.has_key(k1):    
                      s= "%s\t%s\t%s\t%s\t%s\t%s"% (
                               "object:%s precipitant: %s "%(pddiL[0].get("object") ,pddiL[0].get("precipitant"))
                              ,"%s Evidence: %s "%(pddiL[0].get("source") ,pddiL[0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d2[k1][0].get("source") ,d2[k1][0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d3[k1][0].get("source") ,d3[k1][0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d4[k1][0].get("source") ,d4[k1][0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d5[k1][0].get("source") ,d5[k1][0].get("evidenceStatement"))
                               )
                      #print s     
                      common[k1] =s  
                          
        if d2.has_key(k2):  
            if d3.has_key(k2): 
                if d4.has_key(k2):  
                    if d5.has_key(k2):   
                      s= "%s\t%s\t%s\t%s\t%s\t%s" % (
                               "object:%s precipitant: %s "%(pddiL[0].get("object") ,pddiL[0].get("precipitant"))
                              ,"%s Evidence: %s "%(pddiL[0].get("source") ,pddiL[0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d2[k2][0].get("source") ,d2[k2][0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d3[k2][0].get("source") ,d3[k2][0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d4[k2][0].get("source") ,d4[k2][0].get("evidenceStatement"))
                              ,"%s Evidence: %s "%(d5[k2][0].get("source") ,d5[k2][0].get("evidenceStatement"))
                              )
                      #print s
                      common[k2] =s
#       
    return (common)
   

def analyzeFiveDataSetOverlap(Name1,Pickle1,Name2,Pickle2,Name3,Pickle3,Name4,Pickle4,Name5,Pickle5):
    
    Dataset_1_Pairs = mapDrugPairs(Pickle1)
    Dataset_2_Pairs = mapDrugPairs(Pickle2) 
    Dataset_3_Pairs = mapDrugPairs(Pickle3) 
    Dataset_4_Pairs = mapDrugPairs(Pickle4) 
    Dataset_5_Pairs = mapDrugPairs(Pickle5) 

    (commonForAll) = findOverlapFiveSets(Dataset_1_Pairs,Dataset_2_Pairs,Dataset_3_Pairs
                                        ,Dataset_4_Pairs,Dataset_5_Pairs )
    
    #write data
    writeCommonPDDIs("../analysis-results/common"+Name1+Name2+Name3+Name4+Name5+".csv",commonForAll)
   
    # report
    print '''Five Source Overlap Analysis 
    Number of PDDIs: 
      ''' +Name1+''': %d '''%len(Dataset_1_Pairs)+'''
      ''' +Name2+''': %d '''%len(Dataset_2_Pairs)+'''
      ''' +Name3+''': %d '''%len(Dataset_3_Pairs)+'''
      ''' +Name4+''': %d '''%len(Dataset_4_Pairs)+'''
      ''' +Name5+''': %d '''%len(Dataset_5_Pairs)+''' 
    Overlap : %d '''%len(commonForAll)+'''
 
 ------------------------------------------------------------------------------------------        
     ''' 

def analyzeFourDataSetOverlap(Name1,Pickle1,Name2,Pickle2,Name3,Pickle3,Name4,Pickle4):
    
    Dataset_1_Pairs = mapDrugPairs(Pickle1)
    Dataset_2_Pairs = mapDrugPairs(Pickle2) 
    Dataset_3_Pairs = mapDrugPairs(Pickle3) 
    Dataset_4_Pairs = mapDrugPairs(Pickle4)   

    (commonForAll) = findOverlapFourSets(Dataset_1_Pairs,Dataset_2_Pairs,Dataset_3_Pairs,Dataset_4_Pairs )
   
   
    # write data
    writeCommonPDDIs("../analysis-results/common"+Name1+Name2+Name3+Name4+".csv", commonForAll)
   
    # report
    print '''Four Source Overlap Analysis 
    Number of PDDIs: 
      ''' +Name1+''': %d '''%len(Dataset_1_Pairs)+'''
      ''' +Name2+''': %d '''%len(Dataset_2_Pairs)+'''
      ''' +Name3+''': %d '''%len(Dataset_3_Pairs)+'''
      ''' +Name4+''': %d '''%len(Dataset_4_Pairs)+''' 
    Overlap : %d '''%len(commonForAll)+'''
 
 ------------------------------------------------------------------------------------------        
     ''' 
      
def analyzeThreeDataSetOverlap(Name1,Pickle1,Name2,Pickle2,Name3,Pickle3):
    
    Dataset_1_Pairs = mapDrugPairs(Pickle1)
    Dataset_2_Pairs = mapDrugPairs(Pickle2) 
    Dataset_3_Pairs = mapDrugPairs(Pickle3)  

    (commonForAll) = findOverlapThreeSets(Dataset_1_Pairs,Dataset_2_Pairs,Dataset_3_Pairs )
   
   
    # write data
    writeCommonPDDIs("../analysis-results/common"+Name1+Name2+Name3+".csv", commonForAll)
   
    # report
    print '''Three Source Overlap Analysis 
    Number of PDDIs: 
      ''' +Name1+''': %d '''%len(Dataset_1_Pairs)+'''
      ''' +Name2+''': %d '''%len(Dataset_2_Pairs)+'''
      ''' +Name3+''': %d '''%len(Dataset_3_Pairs)+''' 
    Overlap : %d '''%len(commonForAll)+'''
 
 ------------------------------------------------------------------------------------------        
     ''' 
    
    
def analyzeTwoDataSetOverlap(Name1,Pickle1,Name2,Pickle2):
    
    Dataset_1_Pairs = mapDrugPairs(Pickle1)
    Dataset_2_Pairs = mapDrugPairs(Pickle2) 

    (commonForAll) = findOverlapTwoSets(Dataset_1_Pairs,Dataset_2_Pairs )
   
   
    # write data
    writeCommonPDDIs("../analysis-results/common"+Name1+Name2+".csv", commonForAll)
   
    # report
    print '''Two Source Overlap Analysis 
    Number of PDDIs: 
      ''' +Name1+''': %d '''%len(Dataset_1_Pairs)+'''
      ''' +Name2+''': %d '''%len(Dataset_2_Pairs)+''' 
    Overlap : %d '''%len(commonForAll)+'''
 
 ------------------------------------------------------------------------------------------        
     ''' 
    
    
      
def runClinicalSourceOverlap():
    CREDIBLEMEDS_L = loadPickle(CREDIBLEMEDS_PDDI_FILE)   
    NDFRT_L = loadPickle(NDFRT_PDDI_FILE_INCHI_OR)       
    ONCHIGHPRIORITY_L = loadPickle(ONCHIGHPRIORITY_PDDI_FILE)  
    ONCNONINTERUPTIVE_L = loadPickle(ONCNONINTERUPTIVE_PDDI_FILE)  
    OSCAR_L = loadPickle(OSCAR_PDDI_FILE)    
     
    #Clinical Sources Analysis    
    analyzeFiveDataSetOverlap("CredibleMeds",CREDIBLEMEDS_L,"NDFRT",NDFRT_L,"ONC-HighPriority",ONCHIGHPRIORITY_L
                              ,"ONC-NonInteruptive",ONCNONINTERUPTIVE_L,"OSCAR",OSCAR_L)
     
    analyzeFourDataSetOverlap("NDFRT",NDFRT_L,"ONC-HighPriority",ONCHIGHPRIORITY_L,"ONC-NonInteruptive",ONCNONINTERUPTIVE_L
                              ,"OSCAR",OSCAR_L) 
    analyzeFourDataSetOverlap("CredibleMeds",CREDIBLEMEDS_L,"ONC-HighPriority",ONCHIGHPRIORITY_L,"ONC-NonInteruptive",ONCNONINTERUPTIVE_L
                              ,"OSCAR",OSCAR_L) 
    analyzeFourDataSetOverlap("CredibleMeds",CREDIBLEMEDS_L,"NDFRT",NDFRT_L,"ONC-NonInteruptive",ONCNONINTERUPTIVE_L
                              ,"OSCAR",OSCAR_L) 
    analyzeFourDataSetOverlap("CredibleMeds",CREDIBLEMEDS_L,"NDFRT",NDFRT_L,"ONC-HighPriority",ONCHIGHPRIORITY_L
                              ,"ONC-NonInteruptive",ONCNONINTERUPTIVE_L) 
    
    analyzeThreeDataSetOverlap("CredibleMeds",CREDIBLEMEDS_L,"NDFRT",NDFRT_L,"ONC-HighPriority",ONCHIGHPRIORITY_L) 
    analyzeThreeDataSetOverlap("CredibleMeds",CREDIBLEMEDS_L,"NDFRT",NDFRT_L,"ONC-NonInteruptive",ONCNONINTERUPTIVE_L) 
    analyzeThreeDataSetOverlap("CredibleMeds",CREDIBLEMEDS_L,"NDFRT",NDFRT_L,"OSCAR",OSCAR_L) 
    analyzeThreeDataSetOverlap("CredibleMeds",CREDIBLEMEDS_L,"ONC-HighPriority",ONCHIGHPRIORITY_L,"ONC-NonInteruptive",ONCNONINTERUPTIVE_L) 
    analyzeThreeDataSetOverlap("CredibleMeds",CREDIBLEMEDS_L,"ONC-HighPriority",ONCHIGHPRIORITY_L,"OSCAR",OSCAR_L) 
    analyzeThreeDataSetOverlap("CredibleMeds",CREDIBLEMEDS_L,"ONC-NonInteruptive",ONCNONINTERUPTIVE_L,"OSCAR",OSCAR_L) 
    analyzeThreeDataSetOverlap("NDFRT",NDFRT_L,"ONC-HighPriority",ONCHIGHPRIORITY_L,"ONC-NonInteruptive",ONCNONINTERUPTIVE_L) 
    analyzeThreeDataSetOverlap("NDFRT",NDFRT_L,"ONC-HighPriority",ONCHIGHPRIORITY_L,"OSCAR",OSCAR_L) 
    analyzeThreeDataSetOverlap("NDFRT",NDFRT_L,"ONC-NonInteruptive",ONCNONINTERUPTIVE_L,"OSCAR",OSCAR_L) 
    analyzeThreeDataSetOverlap("ONC-HighPriority",ONCHIGHPRIORITY_L,"ONC-NonInteruptive",ONCNONINTERUPTIVE_L,"OSCAR",OSCAR_L) 
    
def runNLPSourceOverlap():
    
    DDICORPUS2011_L = loadPickle(DDICORPUS2011_PDDI_FILE_INCHI_OR) 
    DDICORPUS2013_L = loadPickle(DDICORPUS2013_PDDI_FILE_INCHI_OR) 
    PKCORPUS_L = loadPickle(PKCORPUS_PDDI_FILE_INCHI_OR)
    NLMCORPUS_L = loadPickle(NLMCORPUS_PDDI_FILE_INCHI_OR) 
             
    #NLP Sources Analysis     
    analyzeFourDataSetOverlap("DDI-CORPUS-2011",DDICORPUS2011_L,"DDI-CORPUS-2013",DDICORPUS2013_L,
                              "PK-CORPUS",PKCORPUS_L,"NLM-CORPUS",NLMCORPUS_L) 
    
    analyzeThreeDataSetOverlap("DDI-CORPUS-2011",DDICORPUS2011_L,"DDI-CORPUS-2013",DDICORPUS2013_L,"PK-CORPUS",PKCORPUS_L) 
    analyzeThreeDataSetOverlap("DDI-CORPUS-2011",DDICORPUS2011_L,"DDI-CORPUS-2013",DDICORPUS2013_L,"NLM-CORPUS",NLMCORPUS_L) 
    analyzeThreeDataSetOverlap("DDI-CORPUS-2013",DDICORPUS2013_L, "PK-CORPUS",PKCORPUS_L,"NLM-CORPUS",NLMCORPUS_L) 
    analyzeThreeDataSetOverlap("DDI-CORPUS-2011",DDICORPUS2011_L, "PK-CORPUS",PKCORPUS_L,"NLM-CORPUS",NLMCORPUS_L) 
 
 
def runBioinformaticsSourceOverlap():
            
    DIKB_OBSERVED_L = loadPickle(DIKB_OBSERVED_PDDI_FILE)    
    DIKB_PREDICTED_L = loadPickle(DIKB_PREDICTED_PDDI_FILE)   
    allDIKB = ( DIKB_OBSERVED_L + DIKB_PREDICTED_L )    
    KEGG_L = loadPickle(KEGG_PDDI_FILE) 
    DRUGBANK_L = loadPickle(DRUGBANK_PDDI_FILE)   
    TWOSIDES_L = loadPickle(TWOSIDES_PDDI_FILE)    
    SEMMEDDB_L = loadPickle(SEMMEDDB_PDDI_FILE) 


    #Bioinformatics Sources Analysis    
    analyzeFiveDataSetOverlap("DIKB",allDIKB,"KEGG",KEGG_L,"DRUGBANK",DRUGBANK_L
                              ,"TWOSIDES",TWOSIDES_L,"SEMMEDDB",SEMMEDDB_L)
     
    analyzeFourDataSetOverlap("DIKB",allDIKB,"KEGG",KEGG_L,"DRUGBANK",DRUGBANK_L
                              ,"TWOSIDES",TWOSIDES_L) 
    analyzeFourDataSetOverlap("KEGG",KEGG_L,"DRUGBANK",DRUGBANK_L,"TWOSIDES",TWOSIDES_L
                              ,"SEMMEDDB",SEMMEDDB_L) 
    analyzeFourDataSetOverlap("DIKB",allDIKB,"DRUGBANK",DRUGBANK_L,"TWOSIDES",TWOSIDES_L
                              ,"SEMMEDDB",SEMMEDDB_L) 
    analyzeFourDataSetOverlap("DIKB",allDIKB,"KEGG",KEGG_L,"TWOSIDES",TWOSIDES_L
                              ,"SEMMEDDB",SEMMEDDB_L) 
    analyzeFourDataSetOverlap("DIKB",allDIKB,"KEGG",KEGG_L,"DRUGBANK",DRUGBANK_L
                              ,"SEMMEDDB",SEMMEDDB_L) 
        
    analyzeThreeDataSetOverlap("DIKB",allDIKB,"KEGG",KEGG_L,"DRUGBANK",DRUGBANK_L) 
    analyzeThreeDataSetOverlap("DIKB",allDIKB,"KEGG",KEGG_L,"TWOSIDES",TWOSIDES_L) 
    analyzeThreeDataSetOverlap("DIKB",allDIKB,"KEGG",KEGG_L,"SEMMEDDB",SEMMEDDB_L) 
    analyzeThreeDataSetOverlap("DIKB",allDIKB,"DRUGBANK",DRUGBANK_L,"TWOSIDES",TWOSIDES_L) 
    analyzeThreeDataSetOverlap("DIKB",allDIKB,"DRUGBANK",DRUGBANK_L,"SEMMEDDB",SEMMEDDB_L) 
    analyzeThreeDataSetOverlap("DIKB",allDIKB,"TWOSIDES",TWOSIDES_L,"SEMMEDDB",SEMMEDDB_L) 
    analyzeThreeDataSetOverlap("KEGG",KEGG_L,"DRUGBANK",DRUGBANK_L,"TWOSIDES",TWOSIDES_L) 
    analyzeThreeDataSetOverlap("KEGG",KEGG_L,"DRUGBANK",DRUGBANK_L,"SEMMEDDB",SEMMEDDB_L) 
    analyzeThreeDataSetOverlap("KEGG",KEGG_L,"TWOSIDES",TWOSIDES_L,"SEMMEDDB",SEMMEDDB_L)
    analyzeThreeDataSetOverlap("DRUGBANK",DRUGBANK_L,"TWOSIDES",TWOSIDES_L,"SEMMEDDB",SEMMEDDB_L) 
   

def runWorldVistaOverlap_OR_1():      
    NDFRT_L = loadPickle(NDFRT_PDDI_FILE_INCHI_OR)      
    DRUGBANK_L = loadPickle(DRUGBANK_PDDI_FILE)

    WORLDVISTA_L = loadPickle(WORLDVISTA_PDDI_FILE_INCHI_OR) 
            
    #Sources Analysis  
    analyzeThreeDataSetOverlap("NDFRT",NDFRT_L,"WORLDVISTA",WORLDVISTA_L,"DRUGBANK",DRUGBANK_L) 
    analyzeTwoDataSetOverlap("NDFRT",NDFRT_L,"WORLDVISTA",WORLDVISTA_L) 
    analyzeTwoDataSetOverlap("WORLDVISTA",WORLDVISTA_L,"DRUGBANK",DRUGBANK_L)

def runWorldVistaOverlap_AND_1():   
    NDFRT_L = loadPickle(NDFRT_PDDI_FILE_INCHI_AND)  
    DRUGBANK_L = loadPickle(DRUGBANK_PDDI_FILE)   

    WORLDVISTA_L = loadPickle(WORLDVISTA_PDDI_FILE_INCHI_AND)
        
    #Sources Analysis  
    analyzeThreeDataSetOverlap("NDFRT",NDFRT_L,"WORLDVISTA",WORLDVISTA_L,"DRUGBANK",DRUGBANK_L) 
    analyzeTwoDataSetOverlap("NDFRT",NDFRT_L,"WORLDVISTA",WORLDVISTA_L) 
    analyzeTwoDataSetOverlap("WORLDVISTA",WORLDVISTA_L,"DRUGBANK",DRUGBANK_L)

def runWorldVistaOverlap_OR_2():
    ONCHIGHPRIORITY_L = loadPickle(ONCHIGHPRIORITY_PDDI_FILE)  
    ONCNONINTERUPTIVE_L = loadPickle(ONCNONINTERUPTIVE_PDDI_FILE)
    CREDIBLEMEDS_L = loadPickle(CREDIBLEMEDS_PDDI_FILE)
    
    WORLDVISTA_L = loadPickle(WORLDVISTA_PDDI_FILE_INCHI_OR)
                
    #Sources Analysis
    analyzeThreeDataSetOverlap("ONCHIGHPRIORITY",ONCHIGHPRIORITY_L, "CREDIBLEMEDS", CREDIBLEMEDS_L, "WORLDVISTA", WORLDVISTA_L)
    analyzeTwoDataSetOverlap("ONCHIGHPRIORITY",ONCHIGHPRIORITY_L, "WORLDVISTA", WORLDVISTA_L)
    analyzeTwoDataSetOverlap("CREDIBLEMEDS", CREDIBLEMEDS_L, "WORLDVISTA", WORLDVISTA_L)
    analyzeTwoDataSetOverlap("ONCNONINTERUPTIVE", ONCNONINTERUPTIVE_L, "WORLDVISTA", WORLDVISTA_L)

def runWorldVistaOverlap_AND_2():
    ONCHIGHPRIORITY_L = loadPickle(ONCHIGHPRIORITY_PDDI_FILE)  
    ONCNONINTERUPTIVE_L = loadPickle(ONCNONINTERUPTIVE_PDDI_FILE)
    CREDIBLEMEDS_L = loadPickle(CREDIBLEMEDS_PDDI_FILE)
    
    WORLDVISTA_L = loadPickle(WORLDVISTA_PDDI_FILE_INCHI_AND)
                
    #Sources Analysis
    analyzeThreeDataSetOverlap("ONCHIGHPRIORITY",ONCHIGHPRIORITY_L, "CREDIBLEMEDS", CREDIBLEMEDS_L, "WORLDVISTA", WORLDVISTA_L)
    analyzeTwoDataSetOverlap("ONCHIGHPRIORITY",ONCHIGHPRIORITY_L, "WORLDVISTA", WORLDVISTA_L)
    analyzeTwoDataSetOverlap("CREDIBLEMEDS", CREDIBLEMEDS_L, "WORLDVISTA", WORLDVISTA_L)
    analyzeTwoDataSetOverlap("ONCNONINTERUPTIVE", ONCNONINTERUPTIVE_L, "WORLDVISTA", WORLDVISTA_L) 
    
if __name__ == "__main__": 
    
     #runClinicalSourceOverlap()
     #runNLPSourceOverlap()
     #runBioinformaticsSourceOverlap()
     runWorldVistaOverlap_OR_1()
     runWorldVistaOverlap_OR_2()
     
     #runWorldVistaOverlap_AND_1()
     #runWorldVistaOverlap_AND_2()
     
      

   

