#
# analyze-PDDI-overlap-matrix-ADDING-WORLDVISTA.py
#
# Analyze the overlap and differences between sources of knowledge on
# potential drug-drug interactions available on the semantic web -- this time with the addition of WorldVista
#
# Authors: Serkan Ayvaz, Richard D Boyce
#
# February 2016
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
WORLDVISTA_PDDI_FILE_INCHI_AND = "../pickle-data/worldvista-ddis-inchi-and.pickle"
WORLDVISTA_PDDI_FILE_INCHI_OR = "../pickle-data/worldvista-ddis-inchi-or.pickle"

############################################################
# Utility functions
############################################################
 
def loadPickle(FILE_Name):
     f = open(FILE_Name, 'r')
     pickle_file = pickle.load(f)
     f.close()    
     
     return pickle_file
       
def mapDrugPairs(l):
    """ map drug pairs to PDDI dicts. Each key points to a list of PDDIs that share a drug pair """
    d = {}
      
#     for pddi in l:
#         p1=pddi["drug1"]
#         p2=pddi["drug2"]
#         k = "%s-%s" % (p1, p2)
#         if not d.has_key(k):
#             d[k] = [pddi]
#         else:
#             d[k].append(pddi)
   
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
   
def compareD1ToD2(d1, d2):
    """ Comparison is made on the drug pair, not the anticipated event"""
    uniqueToD1 = []
    uniqueToD2 = []
    common = {}
    for key,pddiL in d1.iteritems():
        k1 = "%s-%s" % (pddiL[0]["drug1"], pddiL[0]["drug2"])        
        k2 = "%s-%s" % (pddiL[0]["drug2"], pddiL[0]["drug1"])
        
        if not d2.has_key(k1) and not d2.has_key(k2):
            uniqueToD1.append(k1)
       
        if d2.has_key(k1):
            common[k1] =[pddiL] 
            
        if d2.has_key(k2):
            common[k2] =[pddiL] 
        

    for key,pddiL in d2.iteritems():
        k1 = "%s-%s" % (pddiL[0]["drug1"], pddiL[0]["drug2"])
        k2 = "%s-%s" % (pddiL[0]["drug2"], pddiL[0]["drug1"])
        if k1 in common or k2 in common:
            continue
        else: 
            uniqueToD2.append(k1)

    return (uniqueToD1, uniqueToD2, common)
        
def writeCommonPDDIs(fname,commonL,l1,l2,labelL1,labelL2):
    f = open(fname, "w")
    s = "drug pair    %s    %s\n" % (labelL2, labelL1)
 
    for key,pair in commonL.iteritems():
        s += "%s    [%s]    [%s]\n" % (key, 
                                         ",".join([str((l2[key][0]["uri"] ,l2[key][0]["label"] ))]),  
                                         ",".join([str((pair[0][0]["uri"] ,pair[0][0]["label"]))]))

        
    f.write(s)
    f.close()

def writeUniquePDDIs(fname,uniqueL,l,label):
    f = open(fname, "w")
    s = "drug pair    %s\n" % (label)

    for pair in uniqueL:
        s += "%s    [%s]\n" % (pair, 
                                   ",".join([str((x["uri"],x["label"])) for x in l[pair]]))
    f.write(s)
    f.close()
 
def analyzeDIKBVsDataset(dikbObsL,dikbPredL,Dataset_2_Name,Dataset_2_pickle):
    
    allDIKBL = dikbObsL + dikbPredL  
  
    allDIKBPairs = mapDrugPairs(allDIKBL)
    dikbPredPairs = mapDrugPairs(dikbPredL)
    dikbObsPairs = mapDrugPairs(dikbObsL)
    Dataset_2_Pairs = mapDrugPairs(Dataset_2_pickle) 
    
    # discern common and unique pairs (Does not  assume directionality in terms of the precipitant and object of the PDDI)
    (uniqDIKBAll, uniqDataset_2, commonDIKBAll) = compareD1ToD2(allDIKBPairs, Dataset_2_Pairs)
    (uniqDIKBPred, uniqDataset_2, commonDIKBPred) = compareD1ToD2(dikbPredPairs, Dataset_2_Pairs)
    (uniqDIKBObs, uniqDataset_2, commonDIKBObs) = compareD1ToD2(dikbObsPairs, Dataset_2_Pairs)
  
     
    # write data
    writeCommonPDDIs("../analysis-results/commonDIKBAll"+Dataset_2_Name+".csv",commonDIKBAll, allDIKBPairs, Dataset_2_Pairs, "DIKBAll",Dataset_2_Name)
    #writeCommonPDDIs("../analysis-results/commonDIKBPred"+Dataset_2_Name+".csv",commonDIKBPred, dikbPredPairs, Dataset_2_Pairs, "DIKBPred",Dataset_2_Name)
    #writeCommonPDDIs("../analysis-results/commonDIKBObs"+Dataset_2_Name+".csv",commonDIKBObs, dikbObsPairs, Dataset_2_Pairs, "DIKBObs",Dataset_2_Name)
   
   
    # report
    print ' '' DIKB TO ''' +Dataset_2_Name+  '''
     
    Number of PDDIs: 
      DIKB predicted + observed: %d  '''%len(allDIKBPairs)+'''
      DIKB predicted: %d '''%len(dikbPredPairs)+'''
      DIKB observed: %d '''%len(dikbObsPairs)+'''
      ''' +Dataset_2_Name+''': %d '''%len(Dataset_2_Pairs)+'''

    Overlap DIKB predicted + observed to ''' +Dataset_2_Name+ ''': %d '''%len(commonDIKBAll)+'''
           (%.3f of %s'''%(float(len(commonDIKBAll))/float(len(allDIKBPairs)), 
           "DIKB") + ''',%.3f of %s'''% (float(len(commonDIKBAll))/float(len(Dataset_2_Pairs)), 
           Dataset_2_Name) + ''') 
           
    Overlap DIKB predicted to ''' +Dataset_2_Name+ ''': %d '''%len(commonDIKBPred)+'''
           (%.3f of %s'''%(float(len(commonDIKBPred))/float(len(dikbPredPairs)), 
           "DIKB") + ''',%.3f of %s'''% (float(len(commonDIKBPred))/float(len(Dataset_2_Pairs)), 
           Dataset_2_Name) + ''') 
    
    Overlap DIKB observed to ''' +Dataset_2_Name+ ''': %d '''%len(commonDIKBObs)+'''
           (%.3f of %s'''%(float(len(commonDIKBObs))/float(len(dikbObsPairs)), 
           "DIKB") + ''',%.3f of %s'''% (float(len(commonDIKBObs))/float(len(Dataset_2_Pairs)), 
           Dataset_2_Name) + ''') 
                
 ------------------------------------------------------------------------------------------        
    ''' 

def analyzeDIKBVsDatasets(dikbObsL,dikbPredL,Dataset_2_Name,Dataset_2_pickle, IsConservativeMapping):
    
    allDIKBL = dikbObsL + dikbPredL  
  
    allDIKBPairs = mapDrugPairs(allDIKBL)
    dikbPredPairs = mapDrugPairs(dikbPredL)
    dikbObsPairs = mapDrugPairs(dikbObsL)
    Dataset_2_Pairs = mapDrugPairs(Dataset_2_pickle) 
    
    # discern common and unique pairs (Does not  assume directionality in terms of the precipitant and object of the PDDI)
    (uniqDIKBAll, uniqDataset_2, commonDIKBAll) = compareD1ToD2(allDIKBPairs, Dataset_2_Pairs)
    (uniqDIKBPred, uniqDataset_2, commonDIKBPred) = compareD1ToD2(dikbPredPairs, Dataset_2_Pairs)
    (uniqDIKBObs, uniqDataset_2, commonDIKBObs) = compareD1ToD2(dikbObsPairs, Dataset_2_Pairs)
  
     
    # write data 
    if IsConservativeMapping:
        writeCommonPDDIs("../analysis-results/commonDIKBAll"+Dataset_2_Name+"_INCHI_AND.csv",commonDIKBAll, allDIKBPairs, Dataset_2_Pairs, "DIKBAll",Dataset_2_Name)
    else:
       writeCommonPDDIs("../analysis-results/commonDIKBAll"+Dataset_2_Name+"_INCHI_OR.csv",commonDIKBAll, allDIKBPairs, Dataset_2_Pairs, "DIKBAll",Dataset_2_Name)
    
    #writeCommonPDDIs("../analysis-results/commonDIKBPred"+Dataset_2_Name+".csv",commonDIKBPred, dikbPredPairs, Dataset_2_Pairs, "DIKBPred",Dataset_2_Name)
    #writeCommonPDDIs("../analysis-results/commonDIKBObs"+Dataset_2_Name+".csv",commonDIKBObs, dikbObsPairs, Dataset_2_Pairs, "DIKBObs",Dataset_2_Name)
   
   
    # report
    print ' '' DIKB TO ''' +Dataset_2_Name+  '''
     
    Number of PDDIs: 
      DIKB predicted + observed: %d  '''%len(allDIKBPairs)+'''
      DIKB predicted: %d '''%len(dikbPredPairs)+'''
      DIKB observed: %d '''%len(dikbObsPairs)+'''
      ''' +Dataset_2_Name+''': %d '''%len(Dataset_2_Pairs)+'''

    Overlap DIKB predicted + observed to ''' +Dataset_2_Name+ ''': %d '''%len(commonDIKBAll)+'''
           (%.3f of %s'''%(float(len(commonDIKBAll))/float(len(allDIKBPairs)), 
           "DIKB") + ''',%.3f of %s'''% (float(len(commonDIKBAll))/float(len(Dataset_2_Pairs)), 
           Dataset_2_Name) + ''') 
           
    Overlap DIKB predicted to ''' +Dataset_2_Name+ ''': %d '''%len(commonDIKBPred)+'''
           (%.3f of %s'''%(float(len(commonDIKBPred))/float(len(dikbPredPairs)), 
           "DIKB") + ''',%.3f of %s'''% (float(len(commonDIKBPred))/float(len(Dataset_2_Pairs)), 
           Dataset_2_Name) + ''') 
    
    Overlap DIKB observed to ''' +Dataset_2_Name+ ''': %d '''%len(commonDIKBObs)+'''
           (%.3f of %s'''%(float(len(commonDIKBObs))/float(len(dikbObsPairs)), 
           "DIKB") + ''',%.3f of %s'''% (float(len(commonDIKBObs))/float(len(Dataset_2_Pairs)), 
           Dataset_2_Name) + ''') 
                
 ------------------------------------------------------------------------------------------        
    '''             

def analyzeDataset(Dataset_1_Name,Dataset_1_pickle,Dataset_2_Name,Dataset_2_pickle):
     
    Dataset_1_Pairs = mapDrugPairs(Dataset_1_pickle)
    Dataset_2_Pairs = mapDrugPairs(Dataset_2_pickle) 
    
    # discern common and unique pairs (Does not  assume directionality in terms of the precipitant and object of the PDDI)
    (uniqDataset_1, uniqDataset_2, common) = compareD1ToD2(Dataset_1_Pairs, Dataset_2_Pairs)
 
    # write data
    writeCommonPDDIs("../analysis-results/common"+Dataset_1_Name+Dataset_2_Name+".csv", 
                     common, Dataset_1_Pairs, Dataset_2_Pairs, Dataset_1_Name,Dataset_2_Name)
   
    # report
    print ' '+Dataset_1_Name+ ''' TO ''' +Dataset_2_Name+  '''

    Number of PDDIs: 
      ''' +Dataset_1_Name+''': %d '''%len(Dataset_1_Pairs)+'''
      ''' +Dataset_2_Name+''': %d '''%len(Dataset_2_Pairs)+'''

    Overlap '''+Dataset_1_Name+''' to ''' +Dataset_2_Name+ ''': %d '''%len(common)+'''
           (%.3f of %s'''%(float(len(common))/float(len(Dataset_1_Pairs)), 
           Dataset_1_Name) + ''',%.3f of %s'''% (float(len(common))/float(len(Dataset_2_Pairs)), 
           Dataset_2_Name) + ''') 
 
 ------------------------------------------------------------------------------------------        
     ''' 

def analyzeDatasets(Dataset_1_Name,Dataset_1_pickle,Dataset_2_Name,Dataset_2_pickle, IsConservativeMapping):
     
    Dataset_1_Pairs = mapDrugPairs(Dataset_1_pickle)
    Dataset_2_Pairs = mapDrugPairs(Dataset_2_pickle) 
    
    # discern common and unique pairs (Does not  assume directionality in terms of the precipitant and object of the PDDI)
    (uniqDataset_1, uniqDataset_2, common) = compareD1ToD2(Dataset_1_Pairs, Dataset_2_Pairs)
 
    # write data
    if IsConservativeMapping:
        writeCommonPDDIs("../analysis-results/common"+Dataset_1_Name+Dataset_2_Name+"_INCHI_AND.csv", 
                         common, Dataset_1_Pairs, Dataset_2_Pairs, Dataset_1_Name,Dataset_2_Name)
    else:
        writeCommonPDDIs("../analysis-results/common"+Dataset_1_Name+Dataset_2_Name+"_INCHI_OR.csv", 
                         common, Dataset_1_Pairs, Dataset_2_Pairs, Dataset_1_Name,Dataset_2_Name)
    
    # report
    print ' '+Dataset_1_Name+ ''' TO ''' +Dataset_2_Name+  '''

    Number of PDDIs: 
      ''' +Dataset_1_Name+''': %d '''%len(Dataset_1_Pairs)+'''
      ''' +Dataset_2_Name+''': %d '''%len(Dataset_2_Pairs)+'''

    Overlap '''+Dataset_1_Name+''' to ''' +Dataset_2_Name+ ''': %d '''%len(common)+'''
           (%.3f of %s'''%(float(len(common))/float(len(Dataset_1_Pairs)), 
           Dataset_1_Name) + ''',%.3f of %s'''% (float(len(common))/float(len(Dataset_2_Pairs)), 
           Dataset_2_Name) + ''') 
 
 ------------------------------------------------------------------------------------------        
     ''' 
 
 
if __name__ == "__main__": 
   
    IsConservativeMapping=False
    
    #Load the pickle files once and use for multiple times to avoid multiple pickle loadings
    DIKB_OBSERVED_L = loadPickle(DIKB_OBSERVED_PDDI_FILE)    
    DIKB_PREDICTED_L = loadPickle(DIKB_PREDICTED_PDDI_FILE)   
    DRUGBANK_L = loadPickle(DRUGBANK_PDDI_FILE)   
    TWOSIDES_L = loadPickle(TWOSIDES_PDDI_FILE)    
    KEGG_L = loadPickle(KEGG_PDDI_FILE) 
    CREDIBLEMEDS_L = loadPickle(CREDIBLEMEDS_PDDI_FILE)       
    ONCHIGHPRIORITY_L = loadPickle(ONCHIGHPRIORITY_PDDI_FILE)  
    ONCNONINTERUPTIVE_L = loadPickle(ONCNONINTERUPTIVE_PDDI_FILE)  
    OSCAR_L = loadPickle(OSCAR_PDDI_FILE) 
    SEMMEDDB_L = loadPickle(SEMMEDDB_PDDI_FILE)   

    if IsConservativeMapping:
        NDFRT_L = loadPickle(NDFRT_PDDI_FILE_INCHI_AND)    
        DDICORPUS2011_L = loadPickle(DDICORPUS2011_PDDI_FILE_INCHI_AND) 
        DDICORPUS2013_L = loadPickle(DDICORPUS2013_PDDI_FILE_INCHI_AND) 
        NLMCORPUS_L = loadPickle(NLMCORPUS_PDDI_FILE_INCHI_AND) 
        PKCORPUS_L = loadPickle(PKCORPUS_PDDI_FILE_INCHI_AND)
        WORLDVISTA_L = loadPickle(WORLDVISTA_PDDI_FILE_INCHI_AND)
    else: 
        NDFRT_L = loadPickle(NDFRT_PDDI_FILE_INCHI_OR)    
        DDICORPUS2011_L = loadPickle(DDICORPUS2011_PDDI_FILE_INCHI_OR) 
        DDICORPUS2013_L = loadPickle(DDICORPUS2013_PDDI_FILE_INCHI_OR) 
        NLMCORPUS_L = loadPickle(NLMCORPUS_PDDI_FILE_INCHI_OR) 
        PKCORPUS_L = loadPickle(PKCORPUS_PDDI_FILE_INCHI_OR)
        WORLDVISTA_L = loadPickle(WORLDVISTA_PDDI_FILE_INCHI_OR) 
                  
    #WorldVista Analysis
    analyzeDataset("WORLDVISTA",WORLDVISTA_L,"DIKBAll", DIKB_OBSERVED_L + DIKB_PREDICTED_L)
    analyzeDataset("WORLDVISTA",WORLDVISTA_L,"DrugBank",DRUGBANK_L)
    analyzeDataset("WORLDVISTA",WORLDVISTA_L,"Twosides",TWOSIDES_L)
    analyzeDatasets("WORLDVISTA",WORLDVISTA_L,"NDFRT",NDFRT_L,IsConservativeMapping)
    analyzeDataset("WORLDVISTA",WORLDVISTA_L,"KEGG",KEGG_L)
    analyzeDataset("WORLDVISTA",WORLDVISTA_L,"CredibleMeds",CREDIBLEMEDS_L)
    analyzeDatasets("WORLDVISTA",WORLDVISTA_L,"DDICorpus2011",DDICORPUS2011_L,IsConservativeMapping)
    analyzeDatasets("WORLDVISTA",WORLDVISTA_L,"DDICorpus2013",DDICORPUS2013_L,IsConservativeMapping)
    analyzeDatasets("WORLDVISTA",WORLDVISTA_L,"NLMCorpus",NLMCORPUS_L,IsConservativeMapping)
    analyzeDatasets("WORLDVISTA",WORLDVISTA_L,"PKCorpus",PKCORPUS_L,IsConservativeMapping)
    analyzeDataset("WORLDVISTA",WORLDVISTA_L,"ONCHighPriority",ONCHIGHPRIORITY_L)
    analyzeDataset("WORLDVISTA",WORLDVISTA_L,"ONCNonInteruptive",ONCNONINTERUPTIVE_L)
    analyzeDataset("WORLDVISTA",WORLDVISTA_L,"OSCAR",OSCAR_L)
    analyzeDataset("WORLDVISTA",WORLDVISTA_L,"SemMedDB",SEMMEDDB_L)
        
        
    # #DIKB Analysis
    # analyzeDIKBVsDataset(DIKB_OBSERVED_L,DIKB_PREDICTED_L,"DrugBank",DRUGBANK_L)
    # analyzeDIKBVsDataset(DIKB_OBSERVED_L,DIKB_PREDICTED_L,"Twosides",TWOSIDES_L)
    # analyzeDIKBVsDatasets(DIKB_OBSERVED_L,DIKB_PREDICTED_L,"NDFRT",NDFRT_L,IsConservativeMapping)
    # analyzeDIKBVsDataset(DIKB_OBSERVED_L,DIKB_PREDICTED_L,"KEGG",KEGG_L)
    # analyzeDIKBVsDataset(DIKB_OBSERVED_L,DIKB_PREDICTED_L,"CredibleMeds",CREDIBLEMEDS_L)
    # analyzeDIKBVsDatasets(DIKB_OBSERVED_L,DIKB_PREDICTED_L,"DDICorpus2011",DDICORPUS2011_L,IsConservativeMapping)
    # analyzeDIKBVsDatasets(DIKB_OBSERVED_L,DIKB_PREDICTED_L,"DDICorpus2013",DDICORPUS2013_L,IsConservativeMapping)
    # analyzeDIKBVsDatasets(DIKB_OBSERVED_L,DIKB_PREDICTED_L,"NLMCorpus",NLMCORPUS_L,IsConservativeMapping)
    # analyzeDIKBVsDatasets(DIKB_OBSERVED_L,DIKB_PREDICTED_L,"PKCorpus",PKCORPUS_L,IsConservativeMapping)
    # analyzeDIKBVsDataset(DIKB_OBSERVED_L,DIKB_PREDICTED_L,"ONCHighPriority",ONCHIGHPRIORITY_L)
    # analyzeDIKBVsDataset(DIKB_OBSERVED_L,DIKB_PREDICTED_L,"ONCNonInteruptive",ONCNONINTERUPTIVE_L)
    # analyzeDIKBVsDataset(DIKB_OBSERVED_L,DIKB_PREDICTED_L,"OSCAR",OSCAR_L)
    # analyzeDIKBVsDataset(DIKB_OBSERVED_L,DIKB_PREDICTED_L,"SemMedDB",SEMMEDDB_L)
    
    # #Drugbank Analysis
    # analyzeDataset("DrugBank",DRUGBANK_L,"Twosides",TWOSIDES_L)
    # analyzeDatasets("DrugBank",DRUGBANK_L,"NDFRT",NDFRT_L,IsConservativeMapping)
    # analyzeDataset("DrugBank",DRUGBANK_L,"KEGG",KEGG_L)
    # analyzeDataset("DrugBank",DRUGBANK_L,"CredibleMeds",CREDIBLEMEDS_L)
    # analyzeDatasets("DrugBank",DRUGBANK_L,"DDICorpus2011",DDICORPUS2011_L,IsConservativeMapping)
    # analyzeDatasets("DrugBank",DRUGBANK_L,"DDICorpus2013",DDICORPUS2013_L,IsConservativeMapping)
    # analyzeDatasets("DrugBank",DRUGBANK_L,"NLMCorpus",NLMCORPUS_L,IsConservativeMapping)
    # analyzeDatasets("DrugBank",DRUGBANK_L,"PKCorpus",PKCORPUS_L,IsConservativeMapping)
    # analyzeDataset("DrugBank",DRUGBANK_L,"ONCHighPriority",ONCHIGHPRIORITY_L)
    # analyzeDataset("DrugBank",DRUGBANK_L,"ONCNonInteruptive",ONCNONINTERUPTIVE_L)
    # analyzeDataset("DrugBank",DRUGBANK_L,"OSCAR",OSCAR_L)
    # analyzeDataset("DrugBank",DRUGBANK_L,"SemMedDB",SEMMEDDB_L)
  
    # #NDFRT Analysis    
    # analyzeDatasets("NDFRT",NDFRT_L,"Twosides",TWOSIDES_L,IsConservativeMapping)
    # analyzeDatasets("NDFRT",NDFRT_L,"KEGG",KEGG_L,IsConservativeMapping)
    # analyzeDatasets("NDFRT",NDFRT_L,"CredibleMeds",CREDIBLEMEDS_L,IsConservativeMapping)
    # analyzeDatasets("NDFRT",NDFRT_L,"DDICorpus2011",DDICORPUS2011_L,IsConservativeMapping)
    # analyzeDatasets("NDFRT",NDFRT_L,"DDICorpus2013",DDICORPUS2013_L,IsConservativeMapping)
    # analyzeDatasets("NDFRT",NDFRT_L,"NLMCorpus",NLMCORPUS_L,IsConservativeMapping)
    # analyzeDatasets("NDFRT",NDFRT_L,"PKCorpus",PKCORPUS_L,IsConservativeMapping)
    # analyzeDatasets("NDFRT",NDFRT_L,"ONCHighPriority",ONCHIGHPRIORITY_L,IsConservativeMapping)
    # analyzeDatasets("NDFRT",NDFRT_L,"ONCNonInteruptive",ONCNONINTERUPTIVE_L,IsConservativeMapping)
    # analyzeDatasets("NDFRT",NDFRT_L,"OSCAR",OSCAR_L,IsConservativeMapping)
    # analyzeDatasets("NDFRT",NDFRT_L,"SemMedDB",SEMMEDDB_L,IsConservativeMapping)
 
    # #Twosides Analysis 
    # analyzeDataset("Twosides",TWOSIDES_L,"KEGG",KEGG_L)
    # analyzeDataset("Twosides",TWOSIDES_L,"CredibleMeds",CREDIBLEMEDS_L)
    # analyzeDatasets("Twosides",TWOSIDES_L,"DDICorpus2011",DDICORPUS2011_L,IsConservativeMapping)
    # analyzeDatasets("Twosides",TWOSIDES_L,"DDICorpus2013",DDICORPUS2013_L,IsConservativeMapping)
    # analyzeDatasets("Twosides",TWOSIDES_L,"NLMCorpus",NLMCORPUS_L,IsConservativeMapping)
    # analyzeDatasets("Twosides",TWOSIDES_L,"PKCorpus",PKCORPUS_L,IsConservativeMapping)
    # analyzeDataset("Twosides",TWOSIDES_L,"ONCHighPriority",ONCHIGHPRIORITY_L)
    # analyzeDataset("Twosides",TWOSIDES_L,"ONCNonInteruptive",ONCNONINTERUPTIVE_L)
    # analyzeDataset("Twosides",TWOSIDES_L,"OSCAR",OSCAR_L)
    # analyzeDataset("Twosides",TWOSIDES_L,"SemMedDB",SEMMEDDB_L)
   
    # #KEGG Analysis 
    # analyzeDataset("KEGG",KEGG_L,"CredibleMeds",CREDIBLEMEDS_L)
    # analyzeDatasets("KEGG",KEGG_L,"DDICorpus2011",DDICORPUS2011_L,IsConservativeMapping)
    # analyzeDatasets("KEGG",KEGG_L,"DDICorpus2013",DDICORPUS2013_L,IsConservativeMapping)
    # analyzeDatasets("KEGG",KEGG_L,"NLMCorpus",NLMCORPUS_L,IsConservativeMapping)
    # analyzeDatasets("KEGG",KEGG_L,"PKCorpus",PKCORPUS_L,IsConservativeMapping)
    # analyzeDataset("KEGG",KEGG_L,"ONCHighPriority",ONCHIGHPRIORITY_L)
    # analyzeDataset("KEGG",KEGG_L,"ONCNonInteruptive",ONCNONINTERUPTIVE_L)
    # analyzeDataset("KEGG",KEGG_L,"OSCAR",OSCAR_L)
    # analyzeDataset("KEGG",KEGG_L,"SemMedDB",SEMMEDDB_L)
    
    # #CredibleMeds Analysis 
    # analyzeDatasets("CredibleMeds",CREDIBLEMEDS_L,"DDICorpus2011",DDICORPUS2011_L,IsConservativeMapping)
    # analyzeDatasets("CredibleMeds",CREDIBLEMEDS_L,"DDICorpus2013",DDICORPUS2013_L,IsConservativeMapping)
    # analyzeDatasets("CredibleMeds",CREDIBLEMEDS_L,"NLMCorpus",NLMCORPUS_L,IsConservativeMapping)
    # analyzeDatasets("CredibleMeds",CREDIBLEMEDS_L,"PKCorpus",PKCORPUS_L,IsConservativeMapping)
    # analyzeDataset("CredibleMeds",CREDIBLEMEDS_L,"ONCHighPriority",ONCHIGHPRIORITY_L)
    # analyzeDataset("CredibleMeds",CREDIBLEMEDS_L,"ONCNonInteruptive",ONCNONINTERUPTIVE_L)
    # analyzeDataset("CredibleMeds",CREDIBLEMEDS_L,"OSCAR",OSCAR_L)
    # analyzeDataset("CredibleMeds",CREDIBLEMEDS_L,"SemMedDB",SEMMEDDB_L)
     
    # #DDICorpus2011 Analysis 
    # analyzeDatasets("DDICorpus2011",DDICORPUS2011_L,"DDICorpus2013",DDICORPUS2013_L,IsConservativeMapping)
    # analyzeDatasets("DDICorpus2011",DDICORPUS2011_L,"NLMCorpus",NLMCORPUS_L,IsConservativeMapping)
    # analyzeDatasets("DDICorpus2011",DDICORPUS2011_L,"PKCorpus",PKCORPUS_L,IsConservativeMapping)
    # analyzeDatasets("DDICorpus2011",DDICORPUS2011_L,"ONCHighPriority",ONCHIGHPRIORITY_L,IsConservativeMapping)
    # analyzeDatasets("DDICorpus2011",DDICORPUS2011_L,"ONCNonInteruptive",ONCNONINTERUPTIVE_L,IsConservativeMapping)
    # analyzeDatasets("DDICorpus2011",DDICORPUS2011_L,"OSCAR",OSCAR_L,IsConservativeMapping)
    # analyzeDatasets("DDICorpus2011",DDICORPUS2011_L,"SemMedDB",SEMMEDDB_L,IsConservativeMapping)
        
    # #DDICorpus2013 Analysis 
    # analyzeDatasets("DDICorpus2013",DDICORPUS2013_L,"NLMCorpus",NLMCORPUS_L,IsConservativeMapping)
    # analyzeDatasets("DDICorpus2013",DDICORPUS2013_L,"PKCorpus",PKCORPUS_L,IsConservativeMapping)
    # analyzeDatasets("DDICorpus2013",DDICORPUS2013_L,"ONCHighPriority",ONCHIGHPRIORITY_L,IsConservativeMapping)
    # analyzeDatasets("DDICorpus2013",DDICORPUS2013_L,"ONCNonInteruptive",ONCNONINTERUPTIVE_L,IsConservativeMapping)
    # analyzeDatasets("DDICorpus2013",DDICORPUS2013_L,"OSCAR",OSCAR_L,IsConservativeMapping)
    # analyzeDatasets("DDICorpus2013",DDICORPUS2013_L,"SemMedDB",SEMMEDDB_L,IsConservativeMapping)
      
    # #NLMCorpus Analysis  
    # analyzeDatasets("NLMCorpus",NLMCORPUS_L,"PKCorpus",PKCORPUS_L,IsConservativeMapping)
    # analyzeDatasets("NLMCorpus",NLMCORPUS_L,"ONCHighPriority",ONCHIGHPRIORITY_L,IsConservativeMapping)
    # analyzeDatasets("NLMCorpus",NLMCORPUS_L,"ONCNonInteruptive",ONCNONINTERUPTIVE_L,IsConservativeMapping)
    # analyzeDatasets("NLMCorpus",NLMCORPUS_L,"OSCAR",OSCAR_L,IsConservativeMapping)
    # analyzeDatasets("NLMCorpus",NLMCORPUS_L,"SemMedDB",SEMMEDDB_L,IsConservativeMapping)
    
    # #PKCorpus Analysis     
    # analyzeDatasets("PKCorpus",PKCORPUS_L,"ONCHighPriority",ONCHIGHPRIORITY_L,IsConservativeMapping)
    # analyzeDatasets("PKCorpus",PKCORPUS_L,"ONCNonInteruptive",ONCNONINTERUPTIVE_L,IsConservativeMapping)
    # analyzeDatasets("PKCorpus",PKCORPUS_L,"OSCAR",OSCAR_L,IsConservativeMapping)
    # analyzeDatasets("PKCorpus",PKCORPUS_L,"SemMedDB",SEMMEDDB_L,IsConservativeMapping)
       
    # #ONCHighPriority Analysis   
    # analyzeDataset("ONCHighPriority",ONCHIGHPRIORITY_L,"ONCNonInteruptive",ONCNONINTERUPTIVE_L)
    # analyzeDataset("ONCHighPriority",ONCHIGHPRIORITY_L,"OSCAR",OSCAR_L)
    # analyzeDataset("ONCHighPriority",ONCHIGHPRIORITY_L,"SemMedDB",SEMMEDDB_L)
    
    # #ONCNonInteruptive Analysis      
    # analyzeDataset("ONCNonInteruptive",ONCNONINTERUPTIVE_L,"OSCAR",OSCAR_L)
    # analyzeDataset("ONCNonInteruptive",ONCNONINTERUPTIVE_L,"SemMedDB",SEMMEDDB_L)
   
    # #OSCAR Analysis 
    # analyzeDataset("OSCAR",OSCAR_L,"SemMedDB",SEMMEDDB_L)
 
     
