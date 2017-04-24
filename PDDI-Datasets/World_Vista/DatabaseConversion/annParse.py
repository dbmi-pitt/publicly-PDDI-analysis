import csv
DEBUG = True

consequences = {}
mgmtoptions = {}
susptypos = {}
anotes = {}
# access dictionary with annotations[id]['consequence']
# add to dictionary with annotations[id]

# with open('drug_id_and_description-1-1000.ann', 'r') as f:
with open('drug_id_and_description-1001-end.ann', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    ddiId = None
    consequence = []
    for entity, etype, value in reader:
        # entity is T#. etype is Id, ClinicalConsequence, etc. value is #
        # if 'Id tag found:
        #     look for either 'ClinicalConsequence' tag or another 'Id'
        #     if 'ClinicalConsequence' found before 'Id' add to dictionary
        #     if another 'Id' tag found then that is the new Id
        if etype.split()[0] == 'Id' or 'ClinicalConsequence' or 'ManagementOption' or 'SuspectedTypo' or 'AnnotatorNotes':
            if etype.split()[0] == 'Id':
                # etype structured as 'tag x y'
                if DEBUG:
                    print value
                ddiId = value
                consequence = []
                option = []
                typo = []
                note = []
            if etype.split()[0] == 'ClinicalConsequence':
                if DEBUG:
                    print 'CLINICAL CONSEQUENCE'
                    print value
                consequence.append(value)
            elif etype.split()[0] == 'ManagementOption':
                if DEBUG:
                    print 'MANAGEMENT OPTION'
                    print value
                option.append(value)
            elif etype.split()[0] == 'SuspectedTypo':
                if DEBUG:
                    print 'SUSPECTED TYPO'
                    print value
                typo.append(value)
            elif etype.split()[0] == 'AnnotatorNotes':
                if DEBUG:
                    print 'ANNOTATOR NOTE'
                    print value
                note.append(value)
            if consequence:
                consequences[ddiId] = consequence
            if option:
                mgmtoptions[ddiId] = option
            if typo:
                susptypos[ddiId] = typo
            if note:
                anotes[ddiId] = note
if DEBUG:
    print consequences
    print mgmtoptions
    print susptypos
    print anotes

# with open('drug_id_and_description_consequences_1.tsv', 'w') as file:
#     file.writelines(k + '\t' + str(v) + '\n' for k, v in consequences.iteritems())
# with open('drug_id_and_description_mgmt_1.tsv', 'w') as file:
#     file.writelines(k + '\t' + str(v) + '\n' for k, v in mgmtoptions.iteritems())
# with open('drug_id_and_description_typos_1.tsv', 'w') as file:
#     file.writelines(k + '\t' + str(v) + '\n' for k, v in susptypos.iteritems())
# with open('drug_id_and_description_anotes_1.tsv', 'w') as file:
#     file.writelines(k + '\t' + str(v) + '\n' for k, v in anotes.iteritems())

with open('drug_id_and_description_consequences_2.tsv', 'w') as file:
    file.writelines(k + '\t' + str(v) + '\n' for k, v in consequences.iteritems())
with open('drug_id_and_description_mgmt_2.tsv', 'w') as file:
    file.writelines(k + '\t' + str(v) + '\n' for k, v in mgmtoptions.iteritems())
with open('drug_id_and_description_typos_2.tsv', 'w') as file:
    file.writelines(k + '\t' + str(v) + '\n' for k, v in susptypos.iteritems())
with open('drug_id_and_description_anotes_2.tsv', 'w') as file:
    file.writelines(k + '\t' + str(v) + '\n' for k, v in anotes.iteritems())