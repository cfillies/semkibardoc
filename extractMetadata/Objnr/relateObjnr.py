#!/usr/bin/env python
# coding: utf-8
import re
import sys
import pandas as pd
from ast import literal_eval
from typing import Dict

import Objnr.getObjnr as getObjnr
import extract.extractAdresse as extractAdresse
import extract.extractText as extractText
import Adresse.relateAdresse as relateAdresse
import Misc.helpers as helpers
import Misc.schluesselregex as rex


class initHida:
    def __init__(self):
        hidaTabelle = pd.read_csv(r'Dictionaries\hidaData.csv', sep='\t', encoding='utf-8',
                                  usecols=['denkmalStrasse', 'denkmalHausnr', 'denkmaleObjNr',
                                           'denkmaleAdresse', 'denkmalSachbegriff', 'denkmalName'])
        self.strassenListe = hidaTabelle['denkmalStrasse'].tolist()
        self.hnrListe = hidaTabelle['denkmalHausnr'].tolist()
        self.objnrListe = hidaTabelle['denkmaleObjNr'].tolist()
        self.adresseListe = hidaTabelle['denkmaleAdresse'].tolist()
        self.denkmalSachbegriff = hidaTabelle['denkmalSachbegriff'].tolist()
        self.denkmalName = hidaTabelle['denkmalName'].tolist()


def relateObjnr(metadata: Dict, parser: str ='tika'):

    pfad = next(iter(metadata))
    datei = next(iter(metadata[pfad]))
    inhalt = metadata[pfad][datei]['inhalt']
    adressen = metadata[pfad][datei]['adrDict']

    if adressen == {}:
        adressen, adresse, adrName = relateAdresse.findAddress(metadata, parser)

    if inhalt == '':
        inhalt = extractText.getTextContent(metadata, parser)

    objnr, behoerde, objnrMethode = getObjnr.getObjnr(adressen, inhalt)
    return objnr, behoerde, objnrMethode


def getSachbegriff(metadata, einleseMethode):
    pfad = next(iter(metadata))
    datei = next(iter(metadata[pfad]))
    objnrDatei = metadata[pfad][datei]['objnr']

    if objnrDatei == []:
        objnrDatei, dummy1, dummy2 = relateObjnr(metadata, einleseMethode)

    sachb = []

    hida = initHida()

    for objnr in objnrDatei:
        sachb.extend(literal_eval(hida.denkmalSachbegriff[hida.objnrListe.index(objnr)]))

    sachb = list(set(sachb))
    return sachb


def getDenkmalname(metadata, einleseMethode):
    pfad = next(iter(metadata))
    datei = next(iter(metadata[pfad]))
    objnrDatei = metadata[pfad][datei]['objnr']

    if objnrDatei == []:
        objnrDatei, _, _ = relateObjnr(metadata, einleseMethode)

    denkname = []

    hida = initHida()

    for objnr in objnrDatei:
        denkname.extend(literal_eval(hida.denkmalName[hida.objnrListe.index(objnr)]))

    denkname = list(set(denkname))
    return denkname


def objnrDurchPfad(root, files, denkmalStrasse, denkmaleAdresse, denkmalHausnr, denkmaleObjNr,
                   denkmalSachbegriff, denkmalName, deutsch, behoerdenDict, count, foundObjnrPfad,
                   considerPfadundName=True):
    if considerPfadundName:
        dictResult_single = getObjnr.getObjNrAusPfad(root, files, denkmalStrasse, denkmaleAdresse,
                                                     denkmalHausnr, denkmaleObjNr,
                                                     denkmalSachbegriff, denkmalName, deutsch,
                                                     behoerdenDict)

        if (dictResult_single['pfadtreffer']) and (
                'exact_match_adresse' in dictResult_single['pfadtreffer']['method']):
            # mindestens eine Objektnummer konnte für den gesamten Ordner durch den Pfad bestimmt
            # werden. Nur noch die Vorhaben der Dateien in diesem Ordner fehlen.
            count += len(files)
            foundObjnrPfad = True
    else:
        dictResult_single = {}

    try:
        saveObjnr(root, dictResult_single)
    except:
        return dictResult_single, count, foundObjnrPfad

    return dictResult_single, count, foundObjnrPfad


def objnrDurchDatei(root, file, pfadDictFile, einleseMethode, docxVorhanden, deutsch, denkmale,
                    denkmalStrasse, denkmaleAdresse, denkmalHausnr, denkmaleObjNr,
                    denkmalSachbegriff, denkmalName, behoerden, foundObjnrPfad, countDateiname,
                    countInhalt, considerPfadundName=True):
    dictObjnr = {}

    foundObjnrDatei = False  # Diese Angabe wird für die entsprechende Datei geändert, sobald
    # eine Adresse mit  Objektnummer (durch Dateiname, Pfad, oder Inhalt erkannt wird)
    inhaltVorhanden = True  # Annahme. Wenn die Datei keinen lesbaren Inhalt hat, wird diese
    # Angabe im folgenden korrigiert

    inhalt = extractText.getInhalt(root, file, einleseMethode, docxVorhanden)

    if inhalt is None or inhalt == '':
        inhaltVorhanden = False
        inhalt = ''

    dirstr = ''
    for elem in pfadDictFile['pfad']:
        dirstr = dirstr + ' ' + elem

    inhaltMitPfad = root + ' ' + file + ' ' + inhalt + ' ' + dirstr

    if foundObjnrPfad:
        foundObjnrDatei = True

    else:
        if considerPfadundName:
            # Versuch 2: Adresse aus Dateiname entnehmen, da Infos aus Pfad nicht ausreichend
            dictObjnr, countDateiname, \
            foundObjnrDatei = objnrDurchAdresseInDateiname(file,
                                                           deutsch,
                                                           denkmalStrasse,
                                                           denkmaleAdresse,
                                                           denkmalHausnr,
                                                           denkmaleObjNr,
                                                           denkmalSachbegriff,
                                                           denkmalName,
                                                           behoerden,
                                                           countDateiname,
                                                           foundObjnrDatei)

    if (foundObjnrDatei is False) and inhaltVorhanden:
        # Versuch 3: Adresse bzw. Objektnummer aus Inhalt entnehmen, da Infos aus Pfad und
        # Dateiname nicht ausreichend
        # Versuch 3.1.: Objektnummer aus Datei extrahieren
        dictObjnr, countInhalt, foundObjnrDatei = objnrImInhalt(inhalt, denkmale, countInhalt,
                                                                foundObjnrDatei)

    if (foundObjnrDatei is False) and inhaltVorhanden:
        # Versuch 3.2.: Adresse(n) aus Datei-Inhalt extrahieren      
        dictObjnr, countInhalt, foundObjnrDatei = objnrDurchAdresseImInhalt(inhalt, deutsch,
                                                                            behoerden,
                                                                            denkmalStrasse,
                                                                            denkmaleAdresse,
                                                                            denkmalHausnr,
                                                                            denkmaleObjNr,
                                                                            denkmalSachbegriff,
                                                                            denkmalName,
                                                                            countInhalt,
                                                                            foundObjnrDatei)

    try:
        saveObjnr(root, dictObjnr, file)
    except:  # TODO Exception too broad
        return (dictObjnr, inhaltMitPfad, countDateiname, countInhalt, foundObjnrDatei,
                inhaltVorhanden)

    return dictObjnr, inhaltMitPfad, countDateiname, countInhalt, foundObjnrDatei, inhaltVorhanden


def objnrDurchAdresseInDateiname(file, deutsch, denkmalStrasse, denkmaleAdresse, denkmalHausnr,
                                 denkmaleObjNr, denkmalSachbegriff, denkmalName, behoerdenDict,
                                 count, foundObjnrDatei):
    dateiName = re.sub("[a-zA-Z äÄöÖüÜß]+", lambda ele: " " + ele[0] + " ", file)
    dateiName = dateiName.replace('\ ', '').replace('_', ' ')
    adressenAusDateiName, adresseDateiname, strasseDateiname = extractAdresse.getAdresse(dateiName,
                                                                                         deutsch)

    summaryDictDatei = {}
    if adressenAusDateiName:
        summaryDictDatei = getObjnr.getObjnrAdresse(adressenAusDateiName, denkmalStrasse,
                                                    denkmaleAdresse, denkmalHausnr, denkmaleObjNr,
                                                    denkmalSachbegriff, denkmalName, behoerdenDict)

    summaryDictDatei, count, foundObjnrDatei = getObjnr.pruefenObExakt(summaryDictDatei, count,
                                                                       foundObjnrDatei)

    return summaryDictDatei, count, foundObjnrDatei


def objnrImInhalt(inhalt, denkmale, count, foundObjnrDatei):
    dictResult, foundObjnrDatei, count = getObjnr.getObjnrDirekt(inhalt, denkmale, count,
                                                                 foundObjnrDatei)
    return dictResult, count, foundObjnrDatei


def objnrDurchAdresseImInhalt(inhalt, deutsch, behoerden, denkmalStrasse, denkmaleAdresse,
                              denkmalHausnr, denkmaleObjNr, denkmalSachbegriff, denkmalName, count,
                              foundObjnrDatei):
    adressen, adresseInhalt, strassennameInhalt = extractAdresse.getAdresse(
        inhalt.replace('\\', ' ').replace('_', ' '), deutsch)  # inhalt = inhalt.split('§')[0]

    dictResult_singleInhalt = {}

    if adressen:
        dictResult_singleInhalt = getObjnr.getObjnrAdresse(adressen, denkmalStrasse,
                                                           denkmaleAdresse, denkmalHausnr,
                                                           denkmaleObjNr, denkmalSachbegriff,
                                                           denkmalName, behoerden)

    if ('method' in dictResult_singleInhalt):

        deleteEmptyKey = []
        for key in dictResult_singleInhalt.keys():
            if key in ['method', 'behoerde']:
                continue

                # dictResult_singleInhalt = getObjnr.pruefenObBehoerde(dictResult_singleInhalt, key, behoerden)

            keepKey = []
            keepKey2 = []
            if (dictResult_singleInhalt[key]['treffer']['exact_match_adresse']):
                foundObjnrDatei = True
                keepKey = key

            elif (dictResult_singleInhalt[key]['treffer']['exact_match_strasse']):
                dictResult_singleInhalt, foundObjnrDatei, keepKey = getObjnr.pruefenGlaubwuerdigkeit(
                    dictResult_singleInhalt, key, 'exact_match_strasse', inhalt, foundObjnrDatei)

                if (foundObjnrDatei == False) and (
                        dictResult_singleInhalt[key]['treffer']['closest_match']):
                    dictResult_singleInhalt, foundObjnrDatei, keepKey2 = getObjnr.pruefenGlaubwuerdigkeit(
                        dictResult_singleInhalt, key, 'closest_match', inhalt, foundObjnrDatei)
            if (not keepKey) and (not keepKey2):
                deleteEmptyKey.append(key)

        if len(deleteEmptyKey) == len(dictResult_singleInhalt.keys()) - 2:
            # Keine gültigen Adressenkeys (= nur noch 'method' und 'behoerde' haben vielleicht eine Angabe)
            dictResult_singleInhalt['method'] = ''

        for keytopop in deleteEmptyKey:
            dictResult_singleInhalt.pop(keytopop)

    if (foundObjnrDatei == True):
        count += 1

    return dictResult_singleInhalt, count, foundObjnrDatei


"""
def objnrDurchVorhaben

# Muss noch ordentlich implementiert werden: vorhaben nutzen, um Objnr zu bestimmen
for dirc, dirs, files in os.walk(target_dir):
    for file in dictForDemo:

        if file in vorhMatches[dirc].keys() and dictForDemo[file]['Objektnummer'] == []:
            vmTest = vorhMatches[dirc][file]['vorhaben']

            vmTestList = []
            for key in dictForDemo.keys():
                if dictForDemo[key]['Vorhaben'] == vmTest:
                    vmTestList.extend(dictForDemo[key]['Objektnummer'])

            if vmTestList:
                objTest1 = helpers.most_frequent(vmTestList)
                vmTestList.remove(objTest1)
                objTest2 = helpers.most_frequent(vmTestList)
                objTest = [objTest1, objTest2]

                for demoitemI in range(0,len(objTest)):
                    demoitem = objTest[demoitemI]
                    if demoitem not in denkmale.keys():
                        demoitem +=',T'
                    if demoitem in denkmale.keys():
                        if denkmale[demoitem]['Denkmalname']:
                            nameDemo.append(denkmale[demoitem]['Denkmalname'])
                        if denkmale[demoitem]['Sachbegriff']:
                            sachDemo.append(denkmale[demoitem]['Sachbegriff'])

                dictForDemo[file].update({'Objektnummer': objTest})
                dictForDemo[file].update({'Denkmalname' : nameDemo})
                dictForDemo[file].update({'Sachbegriff' : sachDemo})

            objTest = []
            nameDemo = []
            sachDemo = []
            
with open('dictForDemo.json', 'w') as fp:
    json.dump(dictForDemo, fp, indent = 4, ensure_ascii = False)


"""


def saveObjnr(pfad, allVorhDic, dateiname=''):
    outputDir = sys.path[0] + '\outputResult\\'
    outputFilename = 'objnrTreffer'
    if dateiname != '':
        dictToSave = {pfad: {dateiname: allVorhDic}}
    else:
        dictToSave = {pfad: allVorhDic}

    helpers.save(pfad, outputFilename, dictToSave, outputDir)
