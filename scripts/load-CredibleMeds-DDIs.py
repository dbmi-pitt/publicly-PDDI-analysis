""" Simple Python script to build a dictionary of DDIs from the CredibleMeds site"

# Authors: Serkan Ayvaz, Richard D Boyce 
#
# September 2014

# modified: Feb 25, 2017 by Serkan Ayvaz

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

CREDIBLEMEDS_DATA = "../PDDI-Datasets/Crediblemeds/credibleMeds-listing-02262017.txt"

def credibleMeds_Pickle_Generator():
    # open the CREDIBLEMEDS data file and parse it incrementally
    #
    # @returns: a PDDI drug model dictionary containing all of the data in a single
    #           CREDIBLEMEDS PDDI.
   
    pddiDictL = []
    f = open(CREDIBLEMEDS_DATA, 'r')
    
    while 1 :
        if not f:
            f.close()
            raise StopIteration
        
        l = f.readline()
        if l == "":
            f.close()
            break
        else:
            if l.find("object") != -1: # skips header and stops at EOF
               l = f.readline()
         
            elts = l.strip("\n").split("\t")
            pddi = getPDDIDict()
            (pddi["object"], 
             pddi["drug1"],
             pddi["precipitant"], 
             pddi["drug2"],
             pddi["effectConcept"], 
             pddi["ddiPkMechanism"],
             pddi["source"]
             ) = (
                  elts[0], 
                  "http://bio2rdf.org/drugbank:" + str(elts[1]), 
                  elts[2], 
                  "http://bio2rdf.org/drugbank:" + str(elts[3]), 
                  elts[4], 
                  elts[5],  
                  "CredibleMeds"
                  )
            
            print "object: %s: %s-- precipitant:%s : %s" % (pddi["object"],pddi["drug1"],pddi["precipitant"], pddi["drug2"])
            #print "effectConcept: %s:-- ddiPkMechanism: %s" % (pddi["effectConcept"],pddi["ddiPkMechanism"] )
               
            # return the dictionary entry
            pddiDictL.append(pddi) 
         
    return pddiDictL       
   

if __name__ == "__main__":

    gen=credibleMeds_Pickle_Generator()  
    f = open("../pickle-data/crediblemeds-ddis.pickle","w")
    pickle.dump(gen, f)
    f.close()

