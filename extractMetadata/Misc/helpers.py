#!/usr/bin/env python
# coding: utf-8    
import os
import json
from datetime import datetime
from pathlib import Path


# Helper functions
# Find most frequent element in a list
def most_frequent(list_):
    if list_:
        return max(set(list_), key=list_.count)
    else:
        return []


def filename_divider(filename):
    fname, fext = os.path.splitext(filename)
    # print('before: ',fname)
    fnameNew = fname.replace(".", " ").replace("_", " ").replace("-", " ").replace("'",
                                                                                   " ").replace(
        ",", " ")
    # print('after: ',fnameNew)
    return fnameNew


# def getText(filename):
#     doc = docx.Document(filename)
#     fullText = []
#     for para in doc.paragraphs:
#         fullText.append(para.text)
#     return '\n'.join(fullText)

def printd(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            printd(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


def writeFile(file, root, stringTextFile, outputPath):
    outputfile = outputPath + "vorhabenTreffer.txt"

    if not os.path.isfile(outputfile):
        text_file = open(outputfile, "w", encoding="utf-8")

    text_file.write("\nDateiname: %s\n" % file)
    text_file.write("\n(Pfad: %s)\n" % root)
    text_file.write("%s\n\n\n ------------ \n" % str(stringTextFile))


def save(pfad, outputFilename, dictToSave, outputPath, considerDocName=True):
    if considerDocName:
        outputfile = outputPath + outputFilename + '.json'
    else:
        outputfile = outputPath + + outputFilename + '-NodocName.json'

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    if not os.path.isfile(outputfile):  # create json-result file

        with open(outputfile, 'w') as fp:
            resultFile = dictToSave
            json.dump(resultFile, fp, indent=4, ensure_ascii=False)

    else:  # update the json-result file
        with open(outputfile, 'r') as fp:
            resultFile = json.load(fp)
            resultFile.setdefault(pfad, {}).update(dictToSave[pfad])
        with open(outputfile, 'w') as f:
            json.dump(resultFile, f, indent=4, ensure_ascii=False)


def convertDate(datenDateiAll):
    dtConvert = []
    for dl in datenDateiAll:
        if dl.year > 1950:
            dtConvert.append(dl.strftime('%d/%m/%Y'))

    if not dtConvert:
        dtConvert = ['']

    return dtConvert


def convertstring2date(datestr):
    if datestr == '':
        datestr = '01/01/1000'

    datetime_obj = datetime.strptime(datestr, '%d/%m/%Y')
    return datetime_obj


def save_metadata(metadata, results_path):
    pfad = next(iter(metadata))
    datei = next(iter(metadata[pfad]))

    if not results_path.is_file():
        # create one
        with open(results_path, 'w', encoding="utf-8") as fp:
            json.dump(metadata, fp, indent=4, ensure_ascii=False)

    else:
        # Open and update existing result dictionary (json file), then save it again
        with open(results_path, encoding='utf-8') as f:
            metadata_all = json.load(f)

        if pfad in metadata_all.keys():
            metadata_all[pfad][datei] = metadata[pfad][datei]
        else:
            metadata_all.update(metadata)

        with open(results_path, 'w', encoding="utf-8") as fp:
            json.dump(metadata_all, fp, indent=4, ensure_ascii=False)

    return print("Saved metadata to: ", results_path)


def getDirectory(datei, dateiOrdnerStruktur_path):
    dateiOrdnerStruktur = Path(dateiOrdnerStruktur_path)
    with open(dateiOrdnerStruktur, encoding='utf-8') as f:
        ordnerStruktur = json.load(f)

    reversedDictionary = {}
    count = 0
    countTotal = 0
    repeatedName = []
    directories = []
    outermost_dirLength = 1000

    for dc in ordnerStruktur:

        directories.append(dc['dir'])

        for file in dc['files']:
            countTotal += 1

            if len(dc['dir']) < outermost_dirLength:
                outermost_dirLength = len(dc['dir'])
                outermost_dir = dc['dir']

            if file in reversedDictionary.keys():
                count += 1
                repeatedName.append(file)
            else:
                reversedDictionary[file] = dc['dir']

    # print(str(count) + ' out of ' + str(countTotal) + ' (' + str(round(count/countTotal*100)) \
    #      + '%) files with non-unique names.')

    repeatedNameSet = set(repeatedName)
    for key in repeatedNameSet:
        reversedDictionary.pop(key)

    if datei in reversedDictionary.keys():
        pfad = reversedDictionary[datei]
    else:
        print(
            'Datei hat keinen eindeutigen Name im Datensatz. Pfad kann nicht eindeutig bestimmt werden.')
        print('In diesen Fällen wird der Parent Directory des Datensatz zum "pfad"')
        pfad = outermost_dir

    return pfad, outermost_dir, reversedDictionary, directories


def getFiles(folder, dateiOrdnerStruktur_path):
    dateiOrdnerStruktur = Path(dateiOrdnerStruktur_path)
    with open(dateiOrdnerStruktur) as f:
        ordnerStruktur = json.load(f)

    ordnerStrukturDic = {}
    for dc in ordnerStruktur:
        ordnerStrukturDic[dc['dir']] = dc['files']

    try:
        files = ordnerStrukturDic[folder]
    except:
        files = None

    return files

######
# Datei mit Ordnerstruktur erstellen: 

# import os
# targetDir = 'C:\\Users\\schull\\Projekte\\KIbarDok\\testOrdner'
# ordnerStruktur = []
# dic = {}

# for root,dirs,files in os.walk(targetDir):
#    dic = {'dir' : root, 'files': files}
#    ordnerStruktur.append(dic)

# with open(r'Dictionaries\ordnerStrukturTest.json', 'w', encoding="utf-8") as fp:
#            json.dump(ordnerStruktur, fp, indent = 4, ensure_ascii = False)


###########
# Copy files recursively from one directory to the other

# import shutil

# rootdir = 'C:\\Users\\schull\\Projekte\\KIbarDok\\ghgjhg_testOrdner'
# target = 'C:\\Users\\schull\\Projekte\\KIbarDok\\testDaten'

# for root, dirs, files in os.walk(rootdir):
#    for file in files:
#        #print(root + '\\' + file)
#        shutil.copyfile(root + '\\' + file, target + '\\' + file)
