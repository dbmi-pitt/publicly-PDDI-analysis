""" Simple Python script to build a dictionary of DDIs from the DDI Corpus 2013"

# Authors: Serkan Ayvaz  
#
# Feb 2016

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

sys.path = sys.path + ['.']
from PDDI_Model import getPDDIDict

WorldVista_DATA_INCHI_AND = "../PDDI-Datasets/World_Vista/WorldVistaMappedINCHI_AND.csv"
WorldVista_DATA_INCHI_OR = "../PDDI-Datasets/World_Vista/WorldVistaMappedINCHI_OR.csv"

def WorldVista_Pickle_Generator(datafile):
    # open the World-Vista data file and parse it incrementally
    #
    # @returns: a PDDI drug model dictionary containing all of the data in a single
    #           World-Vista PDDI.
   
    pddiDictL = []

    f = open(datafile, 'r')
    
    while 1 :
        if not f:
            f.close()
            raise StopIteration
        
        l = f.readline()
        if l == "":
            f.close()
            break
        else:
            if l.find("Drug_1") != -1: # skips header and stops at EOF
               l = f.readline()
        
        
        elts = l.strip("\n").split("$")
        pddi = getPDDIDict()
        
        (
         pddi["object"],
         pddi["drug1"],
         pddi["precipitant"],
         pddi["drug2"],
         pddi["severity"],
         pddi["homepage"],
         pddi["ddiPkMechanism"],
         pddi["label"],
         pddi["source"]
        )=(
            elts[0], 
            "http://bio2rdf.org/drugbank:" + str(elts[1]), 
            elts[2], 
            "http://bio2rdf.org/drugbank:" +str(elts[3]),
            elts[4],
            elts[5],
            elts[6],
            elts[7],
            "World-Vista"
          )
           
        #print "ID: %s - object: %s: %s-- precipitant:%s : %s" % (elts[0],pddi["object"],pddi["drug1"],pddi["precipitant"], pddi["drug2"])
        print "object: %s: %s-- precipitant:%s : %s" % (pddi["object"],pddi["drug1"],pddi["precipitant"], pddi["drug2"])
                    
        # return the dictionary entry
        pddiDictL.append(pddi)
                     
    return pddiDictL       
   

if __name__ == "__main__":

    gen=WorldVista_Pickle_Generator(WorldVista_DATA_INCHI_AND)  
    f = open("../pickle-data/worldvista-ddis-inchi-and.pickle","w") 
    pickle.dump(gen, f)
    f.close()
 
    gen=WorldVista_Pickle_Generator(WorldVista_DATA_INCHI_OR)  
    f = open("../pickle-data/worldvista-ddis-inchi-or.pickle","w")
    pickle.dump(gen, f)
    f.close()
