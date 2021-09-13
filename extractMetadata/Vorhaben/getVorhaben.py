#!/usr/bin/env python
# coding: utf-8

import os
import re
from pathlib import Path
import json

from extractMetadata.Misc import helpers, schluesselregex as rex
from extractMetadata.extract import extractAdresse
from extractMetadata.extract import extractDatum
from extractMetadata.extract import extractText


def getVorhaben(text):
    """
    Versucht die Textbausteine
    'Vorhaben:', 'Maßnahme (Kurzbeschreibung):' und
    'Denkmalschutzrechtliche Genehmigung zum Bauvorhaben:'
    im übergebenen `text` zu finden. Gibt den nachfolgenden Textbaustein als Vorhaben zurück.
    """
    vorhaben_bezeichnung = "Vorhaben:"
    start_vorhaben = text.find(vorhaben_bezeichnung)
    delimit = '\n'

    if start_vorhaben == -1:
        vorhaben_bezeichnung = "Maßnahme (Kurzbeschreibung):"
        start_vorhaben = text.find(vorhaben_bezeichnung)
        delimit = '\t'
        if start_vorhaben == -1:
            vorhaben_bezeichnung = "Denkmalschutzrechtliche Genehmigung zum Bauvorhaben:"
            start_vorhaben = text.find(vorhaben_bezeichnung)
            delimit = '\n'
            if start_vorhaben == -1:
                return '', delimit

    vorhaben = ''

    index_vorhaben = start_vorhaben + len(vorhaben_bezeichnung) + 1
    delimLine = 0
    while len(vorhaben) <= 1:
        vorhaben = text[index_vorhaben:].split(delimit)[delimLine].replace('\n', '')
        delimLine += 1

    return vorhaben.strip(), delimit


def loadVorhabenDict(outermost_dir, vorhOntologie, methode):
    vorhabenDict_path = Path(r'extractMetadata\Dictionaries\vorhabenDict.json')
    subdirectories_path = Path(r'extractMetadata\Dictionaries\subdirectories.txt')

    if not vorhabenDict_path.is_file():

        allVorhDic, subdirs = erstellenVorhabenDict(outermost_dir, vorhOntologie, methode)

        with open(vorhabenDict_path, 'w', encoding="utf-8") as fp:
            json.dump(allVorhDic, fp, indent=4, ensure_ascii=False)

        with open(subdirectories_path, 'w') as f:
            for item in subdirs:
                f.write("%s," % item)

        return allVorhDic, subdirs

    else:
        # VorhabenDict Laden
        with open(vorhabenDict_path, encoding='utf-8') as f:
            vorhabenDict = json.load(f)

        subdirs_file = open(subdirectories_path, "r")
        content = subdirs_file.read()
        subdirs = content.split(",")
        subdirs_file.close()

        return vorhabenDict, subdirs


def erstellenVorhabenDict(targetDir, vorhabenOntologie, methode, docxVorhanden=True):
    # Extrahieren der Vorhaben zur Zuordnung der Dateien:
    # gibt ein Verzeichnis mit den aufgelisteten Vorhaben aus

    # Liste mit den Ordnern, unter den es keinen weiteren Ordner gibt
    subdirectories = [x[0] for x in os.walk(targetDir)]

    lowest_dirs = list()

    for root, dirs, files in os.walk(targetDir):
        if not dirs:
            lowest_dirs.append(root)

    allVorhDic = {}
    vorhabenHigherDict = {}
    vorhabenDict = {}

    for lowDir in lowest_dirs:

        # print(lowDir)
        vorhabenDict = extrahierenAlleVorhaben(lowDir, vorhabenOntologie, methode, docxVorhanden)

        if vorhabenDict:
            allVorhDic.update(vorhabenDict)
            # print(vorhabenDict)

        higherDir = lowDir.rsplit('\\', 1)[0]  # move one directory higher

        while (higherDir in subdirectories) and (higherDir not in allVorhDic.keys()):

            # print('+++ higherDir: ' + higherDir)

            vorhabenHigherDict = extrahierenAlleVorhaben(higherDir, vorhabenOntologie, methode,
                                                         docxVorhanden)

            if vorhabenHigherDict:
                allVorhDic.update(vorhabenHigherDict)
                # print(vorhabenHigherDict)

            higherDir = higherDir.rsplit('\\', 1)[0]  # move one directory higher
    # except:
    #    pass

    return allVorhDic, subdirectories


def extrahierenOntologie():
    vorhOntologie_path = Path(r'vorhaben_inv.json')
    if vorhOntologie_path.is_file():
        # file exists
        # Ontologie extrahieren
        with open(vorhOntologie_path, encoding='utf-8') as f:
            vorhOntologieUpper = json.load(f)

        vorhOntologie = {}
        for key in vorhOntologieUpper:
            vorhOntologie[key] = {k.lower(): v for k, v in vorhOntologieUpper[key].items()}
        return vorhOntologie
    else:
        print('Ontologie-Datei im Ordner \'others\' nicht vorhanden')


def extrahierenAlleVorhaben(target_dir, ontologie, methode, docxVorhanden):
    listeVorhaben = []
    dateienVorhaben = []
    preprocessedVorhaben = []
    listeOrt = []
    vorhabenDict = {}

    for root, dirs, files in os.walk(target_dir):

        adresseVorhabenDict = {}

        for i in range(0, len(files)):

            pfadDatei = [files[i], root]

            inhalt = extractText.getTextContent(pfadDatei, methode)

            if (inhalt is None) or (inhalt == ""):
                continue

            inhalt = inhalt.split('§')[0]

            vorhaben, delimit = getVorhaben(inhalt)

            if vorhaben == '':
                continue

            preprocVorhabenInit, [], [] = extractText.preprocessText(vorhaben)
            preprocVorhabenAdresse = [c for c in preprocVorhabenInit
                                      if c not in rex.getRegex(
                                          ' '.join(preprocVorhabenInit)).adresseUnvollstaendig]

            preprocVorhaben = entfernenWennFürVorhabenGleichhueltig(preprocVorhabenAdresse)

            vorhOberbegriffe = []
            for item in preprocVorhaben:
                if item in ontologie['words'].keys():
                    itemsList = [itemUpper.lower() for itemUpper in ontologie['words'][item]]
                    vorhOberbegriffe.extend(itemsList)

            start_grundstück = inhalt.find("Grundstück")

            if start_grundstück != -1:
                index = len('Grundstück') + 1
            else:
                start_grundstück = inhalt.find("Grundstücke")
                index = len('Grundstücke') + 1

            delimLine = 0
            adresseVorhaben = ''

            while len(adresseVorhaben) <= 1:
                adresseVorhaben = inhalt[start_grundstück + index:].split(delimit)[delimLine]
                delimLine += 1
                # Es gab einen Delimiter vor dem eigentlichen Adresse
                # adresseVorhaben = inhalt[start_grundstück+index:].split(delimit)[onefurther]
                # if len(adresseVorhaben) <= 1:
                #    # Es gab einen weiteren Delimiter vor dem eigentlichen Adresse
                #    adresseVorhaben = inhalt[start_grundstück+index:].split(delimit)[1]

            adressenDict, dummy1, dummy2 = extractAdresse.getAddress(
                adresseVorhaben)  # rex.getRegex(adresseVorhaben).adresseUnvollstaendig

            textCleanSpace = re.sub(' +', ' ',
                                    inhalt.replace('\n', ' ').replace('\t', ' ')
                                    .replace('\r', ' ').rstrip())
            datesList = helpers.convertDate(extractDatum.getDates(textCleanSpace))

            adresseVorhabenDict = mergeVorhabenDicts(adressenDict, adresseVorhabenDict, vorhaben,
                                                     preprocVorhaben, vorhOberbegriffe, files[i],
                                                     datesList)

        vorhabenDict[root] = adresseVorhabenDict

    return vorhabenDict  # dateienVorhaben, listeVorhaben, preprocessedVorhaben, listeOrt


def matchVorhaben(preprocessedText, vorhaben):
    text = ' '.join(preprocessedText)

    percContainedVorhaben = []

    if vorhaben == []:
        percContainedVorhaben.append(0.0)

    contained = [x for x in vorhaben if x in text]
    percentContained = round((len(contained) * 100) / len(vorhaben), 2)

    return percentContained


def mergeVorhabenDicts(a, b, vorhaben, prepVorhaben, oberbegriffe, filename, daten):
    # a ist das Zusatz-Wörterbuch
    # b ist das Wörterbuch, was vervollsständigt werden soll 
    for key in a.keys():
        for innerKey in a[key].keys():
            if key in b.keys():
                innerKeyFound = False
                for innerKey2 in b[key].keys():
                    if set(a[key][innerKey]['hausnummer']) == set(b[key][innerKey2]['hausnummer']):
                        innerKeyFound = True

                if not innerKeyFound:
                    # print('noinnerkey')
                    upd_dict1 = {innerKey: a[key][innerKey]}
                    b[key].update(upd_dict1)

            else:
                # print('nokey')
                b[key] = a[key]

            if 'vorhaben' not in b[key][innerKey].keys():
                upd_dict = {'vorhaben': {
                    vorhaben: {'files': [filename], 'datum': sorted(daten, reverse=True),
                               'preproc': prepVorhaben, 'oberbegriffe': oberbegriffe}}}
                b[key][innerKey].update(upd_dict)
            else:
                if vorhaben not in b[key][innerKey]['vorhaben'].keys():
                    upd_dict = {
                        vorhaben: {'files': [filename], 'datum': sorted(daten, reverse=True),
                                   'preproc': prepVorhaben, 'oberbegriffe': oberbegriffe}}
                    b[key][innerKey]['vorhaben'].update(upd_dict)
                else:
                    # print('Information: Vorhaben ist bereits eingetragen.')
                    b[key][innerKey]['vorhaben'][vorhaben]['files'].append(filename)

    return b


def entfernenWennFürVorhabenGleichhueltig(listWords):
    listWordsBereinigt = []
    for word in listWords:
        # remove words that do not help identifying the Vorhaben
        newword = re.sub(
            (r"antrag|anlage|genehmigung|anlage|bauvorhaben|denkmalschutz|anhören|versagen"
             r"|bescheid|stellungnahme|protokoll"),
            "", word)
        listWordsBereinigt.append(newword)

    # remove strings with only digits
    listWordsBereinigtNoDigit = [x for x in listWordsBereinigt if not all(c.isdigit() for c in x)]

    return listWordsBereinigtNoDigit


def explizitesVorhaben(text, moeglVorh, score):
    forTextFile = ''
    tempVorh = getVorhaben(text)[0]

    vorhabenBestMatch = []
    if len(tempVorh) > 2:
        # Datei hat explizites Vorhaben
        if tempVorh not in moeglVorh:
            # Vorhaben ist in der Liste für mögliche Vorhaben dieser Ordner vorhanden
            # (sollte immer so sein)
            forTextFile += (' --> Möglicher Bug: Vorhaben war NICHT in der Liste '
                            'für mögliche Vorhaben dieses Ordners vorhanden: ') + tempVorh + '\n'

        vorhabenBestMatch = tempVorh
        score = -1  # explizites Vorhaben in Datei vorhanden

    return vorhabenBestMatch, score, forTextFile


#############################################################
# Functions to get the matching Vorhaben based on a "ordnerStruktur" (as in
# "OrdnerStrukturTreptow") file instead of actually going recursively
# from one directory to the next


def loadVorhabenDict_OROS(ordnerStruktur, dateidir, directories, vorhOntologie, methode):
    cwd = Path().cwd()
    vorhabenDict_path = cwd / Path(r'Dictionaries\vorhabenDict.json')
    subdirectories_path = cwd / Path(r'Dictionaries\subdirectories.txt')

    if not vorhabenDict_path.is_file():

        allVorhDic = erstellenVorhabenDict_OROS(ordnerStruktur, dateidir, directories,
                                                vorhOntologie, methode)

        with open(vorhabenDict_path, 'w', encoding="utf-8") as fp:
            json.dump(allVorhDic, fp, indent=4, ensure_ascii=False)

        with open(subdirectories_path, 'w') as f:
            for item in directories:
                f.write("%s," % item)

        return allVorhDic, directories

    else:
        # VorhabenDict Laden
        with open(vorhabenDict_path, encoding='utf-8') as f:
            vorhabenDict = json.load(f)

        subdirs_file = open(subdirectories_path, "r")
        content = subdirs_file.read()
        directories = content.split(",")
        subdirs_file.close()

        return vorhabenDict, directories


def erstellenVorhabenDict_OROS(ordnerStruktur, dateidir, subdirectories, vorhOntologie, methode):
    lowest_dirs = []
    countdir = 0

    for dir1 in subdirectories:
        countdir = 0
        for dir2 in subdirectories:
            if dir1 in dir2:
                countdir += 1

        if countdir == 1:
            lowest_dirs.append(dir1)

    allVorhDic = {}
    vorhabenHigherDict = {}
    vorhabenDict = {}

    for lowDir in lowest_dirs:
        files = helpers.getFiles(lowDir, ordnerStruktur)

        if not files:
            vorhabenDict[lowDir] = {}
            allVorhDic.update(vorhabenDict)
            continue

        vorhabenDict = extrahierenAlleVorhaben_OROS(files, dateidir, lowDir, vorhOntologie,
                                                    methode)

        if vorhabenDict:
            allVorhDic.update(vorhabenDict)
            # print(vorhabenDict)

        higherDir = lowDir.rsplit('\\', 1)[0]  # move one directory higher

        while (higherDir in subdirectories) and (higherDir not in allVorhDic.keys()):

            files_higher = helpers.getFiles(higherDir, ordnerStruktur)

            vorhabenHigherDict = extrahierenAlleVorhaben_OROS(files_higher, dateidir, higherDir,
                                                              vorhOntologie, methode)

            if vorhabenHigherDict:
                allVorhDic.update(vorhabenHigherDict)
                # print(vorhabenHigherDict)

            higherDir = higherDir.rsplit('\\', 1)[0]  # move one directory higher
    # except:
    #    pass

    return allVorhDic


def extrahierenAlleVorhaben_OROS(files, directory, directoryOrdnerStruktur, ontologie, methode):
    listeVorhaben = []
    dateienVorhaben = []
    preprocessedVorhaben = []
    listeOrt = []
    vorhabenDict = {}

    adresseVorhabenDict = {}

    for i in range(0, len(files)):

        if not os.path.isfile(directory + '\\' + files[i]):
            # print(files[i] + ' --> not in directory')
            continue

        pfadDatei = [files[i], directory]

        inhalt = extractText.getTextContent(pfadDatei, methode)

        if (inhalt == None) or (inhalt == ""):
            continue

        inhalt = inhalt.split('§')[0]

        vorhaben, delimit = getVorhaben(inhalt)

        if vorhaben == '':
            continue

        preprocVorhabenInit, [], [] = extractText.preprocessText(vorhaben)
        preprocVorhabenAdresse = [c for c in preprocVorhabenInit if c not in rex.getRegex(
            ' '.join(preprocVorhabenInit)).adresseUnvollstaendig]

        preprocVorhaben = entfernenWennFürVorhabenGleichhueltig(preprocVorhabenAdresse)

        vorhOberbegriffe = []
        for item in preprocVorhaben:
            if item in ontologie['words'].keys():
                itemsList = [itemUpper.lower() for itemUpper in ontologie['words'][item]]
                vorhOberbegriffe.extend(itemsList)

        start_grundstück = inhalt.find("Grundstück")

        if start_grundstück != -1:
            index = len('Grundstück') + 1
        else:
            start_grundstück = inhalt.find("Grundstücke")
            index = len('Grundstücke') + 1

        delimLine = 0
        adresseVorhaben = ''

        while len(adresseVorhaben) <= 1:
            adresseVorhaben = inhalt[start_grundstück + index:].split(delimit)[delimLine]
            delimLine += 1
            # Es gab einen Delimiter vor dem eigentlichen Adresse
            # adresseVorhaben = inhalt[start_grundstück+index:].split(delimit)[onefurther]
            # if len(adresseVorhaben) <= 1:
            #    # Es gab einen weiteren Delimiter vor dem eigentlichen Adresse
            #    adresseVorhaben = inhalt[start_grundstück+index:].split(delimit)[1]

        adressenDict, dummy1, dummy2 = extractAdresse.getAddress(
            adresseVorhaben)  # rex.getRegex(adresseVorhaben).adresseUnvollstaendig

        textCleanSpace = re.sub(' +', ' ',
                                inhalt.replace('\n', ' ').replace('\t', ' ').replace('\r',
                                                                                     ' ').rstrip())
        datesList = helpers.convertDate(extractDatum.getDates(textCleanSpace))

        adresseVorhabenDict = mergeVorhabenDicts(adressenDict, adresseVorhabenDict, vorhaben,
                                                 preprocVorhaben, vorhOberbegriffe, files[i],
                                                 datesList)

    vorhabenDict[directoryOrdnerStruktur] = adresseVorhabenDict

    return vorhabenDict  # dateienVorhaben, listeVorhaben, preprocessedVorhaben, listeOrt
