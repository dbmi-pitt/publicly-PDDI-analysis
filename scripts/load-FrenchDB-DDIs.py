""" Simple Python script to build a dictionary of DDIs from the French DDI Referral dataset "

# Authors: Serkan Ayvaz 
#
# March 2017

# modified:  

"""

"#from SPARQLWrapper import SPARQLWrapper, JSON"
import json
import urllib2
import urllib
import traceback
import sys 
import pickle
import re
import time
import csv

sys.path = sys.path + ['.']
from PDDI_Model import getPDDIDict

FRENCHDB_DATA = "../PDDI-Datasets/FrenchDB/frenchDDI.csv"
    
        
def frenchDB_Pickle_Generator():
    # open the FRENCHDB data file and parse it incrementally
    #
    # @returns: a PDDI drug model dictionary containing all of the data in a single
    #           FRENCHDB PDDI.
    # Dataset contains fields:"mol2"(drug2),"mol1"(drug1),"prota2"(class2),"prota1"(class1),
    #                         "description_interaction","mecanisme","niveau"(severity level),
    #                         "DB1"(drug1 Drugbank ID),"DB2"(drug2 Drugbank ID) 
         
   
    pddiDictL = []
    f = open(FRENCHDB_DATA, 'rb')
    reader=csv.reader(f, delimiter='\t', quotechar='|')
     
    while 1 :
        if not f:
            f.close()
            raise StopIteration
        
        l = f.readline()
        if l == "":
            f.close()
            break
        else:
            if l.find("mol1") != -1: # skips header and stops at EOF
               l = f.readline()
  
            elts = l.strip("\n").split("\t")
            pddi = getPDDIDict()
            (pddi["object"], 
             pddi["drug1"],
             pddi["precipitant"], 
             pddi["drug2"],
             pddi["label"], 
             pddi["severity"], 
             pddi["source"]
             ) = (
                  elts[0].strip("\""), 
                  "http://bio2rdf.org/drugbank:" + str(elts[8]).strip("\""), 
                  elts[1].strip("\""), 
                  "http://bio2rdf.org/drugbank:" + str(elts[7]).strip("\""), 
                  elts[4].strip("\""), 
                  elts[6].strip("\""),  
                  "FrenchDB"
                  )
            
            print "object: %s: %s-- precipitant:%s : %s" % (pddi["object"],pddi["drug1"],pddi["precipitant"], pddi["drug2"])
            #print "effectConcept: %s:-- ddiPkMechanism: %s" % (pddi["effectConcept"],pddi["ddiPkMechanism"] )
               
            # return the dictionary entry
            pddiDictL.append(pddi) 
         
    return pddiDictL       
   

if __name__ == "__main__":

    gen=frenchDB_Pickle_Generator()  
    f = open("../pickle-data/frenchDB-ddis.pickle","w")
    pickle.dump(gen, f)
    f.close()
    print("Done")

