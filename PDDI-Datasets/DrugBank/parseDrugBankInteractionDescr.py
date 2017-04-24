'''
parseDrugBankInteractionDescr.py

Created 01/19/2017

@authors: Rich Boyce based on a script by Yifan Ning

@summary: parse drugbank descriptions for drug-drug interactions for the subset of drugs we care about
 
'''

import codecs
from lxml import etree
from lxml.etree import XMLParser, parse
import os, sys
from sets import Set

OUTFILE = "drugbank5-interactions-NLM-R01-drugs.tsv"

NS = "{http://www.drugbank.ca}" 

DRUGLIST = 'AMITRIPTYLINE','AMOXAPINE','APIXABAN','ARIPIPRAZOLE','ASENAPINE','ATORVASTATIN','BENZODIAZEPINE','BUPROPRION','CHLORPROMAZINE','CITALOPRAM','CLOMIPRAMINE','CLOZAPINE','DABIGATRAN','DESIPRAMINE','DESVENLAFAXINE','DOXEPIN','DULOXETINE','ESCITALOPRAM','ESTAZOLAM','ESZOPICLONE','FLUOXETINE','FLUPHENAZINE','FLURAZEPAM','FLUVASTATIN','FLUVOXAMINE','HALOPERIDOL','ILOPERIDONE','IMIPRAMINE','ISOCARBOXAZID','LEVOMILNACIPRAN','LOVASTATIN','LOXAPINE','LURASIDONE','MAPROTILINE','MILNACIPRAN','MIRTAZAPINE','NEFAZODONE','NORTRIPTYLINE','OLANZAPINE','PALIPERIDONE','PAROXETINE','PERPHENAZINE','PHENELZINE','PITAVASTATIN','PRAVASTATIN','PROCHLORPERAZINE','PROTRIPTYLINE','QUAZEPAM','QUETIAPINE','RISPERIDONE','RIVAROXABAN','ROSUVASTATIN','SELEGELINE','SERTRALINE','SIMVASTATIN','TEMAZEPAM','THIORIDAZINE','THIOTHIXENE','TRANYLCYPROMINE','TRIAZOLAM','TRIFLUOPERAZINE','TRIMIPRAMINE','VENLAFAXINE','VILAZODONE','VORTIOXETINE','WARFARIN','ZALEPLON','ZIPRASIDONE','ZOLPIDEM'


'''
data structure of drugbank.xml                                                                                                                                                            
</drug><drug type="small molecule" created="2005-06-13 07:24:05 -0600"                                                                                          
updated="2013-09-16 17:11:29 -0600" version="4.0">                                                                                                              
  <drugbank-id>DB00007</drugbank-id>                                                                                                                            
  <name>Simvastatin</name>                                                                                                                                      
  <property>                                                                                                                                                   
      <kind>InChIKey</kind>                                                                                                         
      <value>InChIKey=RYMZZMVNJRMUDD-HGQWONQESA-N</value>                                                                                                      
      <source>ChemAxon</source>                                                                                                                                
    </property>    

  <synonymns>
   <synonymn>...</synonymn>
   </synonyms>

   <external-identifiers>
    <external-identifier>
    <resource>ChEBI</resource>
    <identifier>6427</identifier>
    </external-identifier>
    </external-identifiers>
'''


if len(sys.argv) > 1:
    DRUGBANK_XML = str(sys.argv[1])
else:
    print "Usage: parseDrugBankInteractionDescr.py <drugbank.xml>"
    sys.exit(1)


## get dict of mappings of drugbank id, name, inchikeys and synonmymns

def parseDrugBankInteractionDescr(root, f):
    for childDrug in root.iter(tag=NS + "drug"):

        subIds = childDrug.findall(NS + "drugbank-id")
        name = childDrug.find(NS + "name")                        
        
        if subIds == None or name == None:
            continue
        else:
            d1Label = name.text
            if d1Label.upper() not in DRUGLIST:
                continue

            drugbankid = None
            for subId in subIds:
                if subId.get("primary") == "true":
                    drugbankid = subId.text

            if drugbankid is None:
                continue
                    
            interactions = childDrug.find(NS + "drug-interactions")
            if interactions is not None:
            
                #print "[INFO] interaction:" 
                for interact in interactions.iter(NS + "drug-interaction"):
                    intDrugId = unicode(interact.find(NS + "drugbank-id").text)
                    #print "intDrugId: " + intDrugId
                    d2Label = unicode(interact.find(NS + "name").text)
                    #print "name: " + name
                    description = unicode(interact.find(NS + "description").text)
                    #print "description: " + description
                    normalizedDesc = description.lower().replace(u' %s' % d1Label.lower(), u" drug1").replace(u' %s' % d2Label.lower(),u" drug2")
                    normalizedDesc = normalizedDesc.lower().replace(u'%s ' % d1Label.lower(),u"drug1 ").replace(u'%s ' % d2Label.lower(),u"drug2 ")
                    
                    f.write(u"%s\t%s\t%s\t%s\t%s\t%s\n" % (d1Label, drugbankid, d2Label, intDrugId, description, normalizedDesc))
                        
def main():
    f = codecs.open(OUTFILE,'w','utf-8')
    p = XMLParser(huge_tree=True, encoding='utf-8')
    tree = parse(DRUGBANK_XML,parser=p)
    root = tree.getroot()
    
    ## mappings of drugbank Id and ChEBI id from drugbank.xml
    parseDrugBankInteractionDescr(root, f)    
    f.close()
    
if __name__ == "__main__":
    main()        



