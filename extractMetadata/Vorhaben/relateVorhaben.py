#!/usr/bin/env python
# coding: utf-8

import os
import sys
import datetime
from operator import itemgetter
import spacy

from extractMetadata.Vorhaben import getVorhaben
from extractMetadata.extract import extractText
from extractMetadata.Adresse import relateAdresse
from extractMetadata.Datum import relateDatum
from extractMetadata.Misc import helpers


class initVorhaben:
    def __init__(self, outermost_dir, methode):
        self.vorhDict_dir = outermost_dir
        self.vorhOntologie = getVorhaben.extrahierenOntologie()
        self.methode = methode
        self.vorhDict, self.subdirs = getVorhaben.loadVorhabenDict(self.vorhDict_dir,
                                                                   self.vorhOntologie,
                                                                   self.methode)
        self.nlp = spacy.load('de_core_news_lg')


class initVorhaben_OROS:
    def __init__(self, ordnerStruktur, dateidir, directories, methode):
        self.vorhDict_dir = directories[0]
        self.vorhOntologie = getVorhaben.extrahierenOntologie()
        self.methode = methode
        self.vorhDict, self.subdirs = getVorhaben.loadVorhabenDict_OROS(ordnerStruktur, dateidir,
                                                                        directories,
                                                                        self.vorhOntologie,
                                                                        self.methode)
        self.nlp = spacy.load('de_core_news_lg')


def vorhaben(metadata, directories, ordnerStruktur, methode):
    target_dir = next(iter(metadata))
    datei = next(iter(metadata[target_dir]))
    dateidir = metadata[target_dir][datei]['pfadAktuell']

    inhalt = metadata[target_dir][datei]['inhalt']
    adressenDict = metadata[target_dir][datei]['adrDict']
    datenStr = metadata[target_dir][datei]['daten']

    if adressenDict == {}:
        adressenDict, adresse, adrName = relateAdresse.findAddress(metadata, methode)

    if inhalt == '':
        inhalt = extractText.getTextContent(metadata, methode)

    if datenStr == []:
        datenStr = relateDatum.datum(metadata, methode)

    daten = [helpers.convertstring2date(i) for i in datenStr]

    if ordnerStruktur == []:
        vorhVars = initVorhaben(directories, methode)
    else:
        outermost_dir = directories[0]
        vorhVars = initVorhaben_OROS(ordnerStruktur, dateidir, directories, methode)

    moeglVorhList, moeglOrtList = getVorhabenListFuerDirectory(target_dir, vorhVars.vorhDict,
                                                               vorhVars.subdirs)

    try:
        vorhabenBestMatch, score = getVorhabenBestMatch(inhalt.split('§')[0], adressenDict, daten,
                                                        moeglVorhList,
                                                        moeglOrtList,
                                                        vorhVars.vorhDict[target_dir],
                                                        vorhVars.vorhOntologie,
                                                        vorhVars.vorhDict_dir, datei)
    except:  # TODO except statement too broad
        vorhabenBestMatch = []
        score = 9999

    return vorhabenBestMatch, score


def getVorhabenListFuerDirectory(pfad, vorhDict, subdirectories):
    moeglVorhList = []
    moeglOrtList = []

    try:
        for key in vorhDict[pfad]:
            for innerkey in vorhDict[pfad][key].keys():
                vorhList = list(vorhDict[pfad][key][innerkey]['vorhaben'].keys())
                moeglVorhList.extend(vorhList)

            if moeglVorhList:
                moeglOrtList.append(key)
    except:
        dummy = 9999

    if not moeglVorhList:

        # Kein Vorhaben in dem Ordner vorhanden, der übergeordnete Ordner wird überprüft        
        higherDir = pfad.rsplit('\\', 1)[0]  # move one directory higher

        while (higherDir in subdirectories) and (moeglVorhList == []):
            try:
                for key in vorhDict[higherDir]:
                    for innerkey in vorhDict[higherDir][key].keys():
                        vorhList = list(vorhDict[higherDir][key][innerkey]['vorhaben'].keys())
                        moeglVorhList.extend(vorhList)

                    if moeglVorhList:
                        moeglOrtList.append(key)
            except:
                dummy = 9999

            higherDir = higherDir.rsplit('\\', 1)[0]  # move one directory higher

    # Nun steht mit dem aktuellen Ordner mindestens ein Vorhaben in Bezug.
    # Im folgenden wird gefrüft, welches der Vorhaben am ehesten zu jedem Dokument passt
    return moeglVorhList, moeglOrtList


def getVorhabenBestMatch(inhalt, adressenDict, datenDateiAll, moeglVorhList, moeglOrt, allVorhDict,
                         vorhOntol, pfad, dateiname):
    score = 11
    vorhabenBestMatch, score, forTextFile = getVorhaben.explizitesVorhaben(inhalt, moeglVorhList,
                                                                           score)

    if not vorhabenBestMatch:

        if datenDateiAll:
            datenDatei = max(datenDateiAll)

        dtMtSort, wtMtSort, obMtSort, adMt = getVorhabenMatches(inhalt, vorhOntol, allVorhDict,
                                                                moeglOrt, adressenDict, datenDatei)

        vorhabenBestMatch, score = matchbewertungScore(vorhabenBestMatch, dtMtSort, wtMtSort,
                                                       obMtSort, adMt, score, moeglVorhList)

        forTextFile += "\nMögliche Vorhaben:\n" + str(moeglVorhList) + "\nMögliche Orte:\n" + str(
            moeglOrt) + "\n"
        forTextFile += "           " + str(dtMtSort) + "\n" + "           " + str(
            wtMtSort) + "\n" + "           " + str(obMtSort) + "\n" + "\n" + "           " + str(
            adMt) + "\n"
        forTextFile += "\nVorhaben, score (0 = höchst, 11 = niedrigst):\n           " + str(
            vorhabenBestMatch) + "," + str(score) + "\n\n\n ------------ \n"
    else:
        forTextFile += "\Explizites Vorhaben, score:\n           " + str(
            vorhabenBestMatch) + "," + str(score) + "\n\n\n ------------ \n"

    dtConvert = []
    for dl in datenDateiAll:
        if dl.year > 1950:
            dtConvert.append(dl.strftime('%d/%m/%Y'))

    dtConvert2 = dtConvert
    if not dtConvert2:
        dtConvert2 = ['']
    vorhabenDict = {'vorhabenBestMatch': vorhabenBestMatch, 'score': score, 'dates': dtConvert2}

    try:
        saveVorhaben(dateiname, pfad, vorhabenDict)
    except:
        return vorhabenBestMatch, score

    return vorhabenBestMatch, score


def matchbewertungScore(vorhabenBestMatch, dtMtSort, wtMtSort, obMtSort, adMt, score,
                        moeglVorhList):
    """
    Kriterien zur Auswahl des Vorhabens:
    - das Datum ist am zuverlässigsten
    - Schlüßelworte sind wichtig, um das Thema zu überprüfen. Möglicherweise
       sind mehrere Vorhaben zu in kurzer Zeit zu einem Denkmal entstanden
    - Der Ort ist wichtig

    Herangehensweise:
    1. Das Vorhaben mit dem kleinsten dt (dtMtSort[0] Datumunterschied zw. Vorhaben und Datei)
    wird bevorzugt.
    2. Scoring wird aufgestellt:
       - Wenn dtMtSort nicht leer ist:
            +1 Punkt
       - Wenn dtMtSort[0] kleiner ist als 90 Tage (3 Monate):
            +4 Punkte; Wenn dtMtSort[0] kleiner ist als 365 Tage (1 Jahr): +2 Punkt
       - Wenn dtMtSort[0] in wtMtSort UND obMtSort vorhanden ist:
            +4 Punkte, Wenn dtMtSort[0] in wtMtSort ODER obMtSort vorhanden ist: +3 Punkte
       - Wenn der Ort, z.B. Akazienhof, zu den aufgelisteten Vorhaben passt:
            +2 Punkt

       - Wenn dtMtSort leer ist, aber wtMtSort gleich obMtSort ist (& beide nicht leer):
            +3 Punkt

       Je niedriger die Punktzahl, desto mehr vertrauen wir das bestimmte Vorhaben. 
       Die beste Punktzahl ist score = -1, also wenn ein explizites Vorhaben in Datei vorhanden ist
       score = 0 ist die bestmögliche Punktzahl bei einem nicht explizit angegebenem Vorhaben
       Der höchste Punktzahl (und somit schlechteste) ist score = 11
       
    """

    if not wtMtSort:
        wtMtSort = [['noMatch', 0]]

    if not obMtSort:
        obMtSort = [['noMatch', 0]]

    score2 = 11

    if dtMtSort:
        indexVorh = 0
        vorhabenBestMatch = dtMtSort[indexVorh][0]
        score -= 1

        wtMtTitle = [item[0] for item in wtMtSort]
        obMtTitle = [item[0] for item in obMtSort]

        if (vorhabenBestMatch in wtMtTitle) and (vorhabenBestMatch in obMtTitle):
            score -= 4
        elif (vorhabenBestMatch in wtMtTitle) or (vorhabenBestMatch in obMtTitle):
            score -= 3
        else:
            if len(dtMtSort) > 1:
                score2 -= 1
                indexVorh2 = 1
                vorhabenBestMatch2 = dtMtSort[indexVorh2][0]

                if (vorhabenBestMatch2 in wtMtTitle) and (vorhabenBestMatch2 in obMtTitle):
                    score2 -= 4
                elif (vorhabenBestMatch2 in wtMtTitle) or (vorhabenBestMatch2 in obMtTitle):
                    score2 -= 3

        if score > score2:
            # Vorhaben unter "score2" zuverlässiger und wird übernommen
            vorhabenBestMatch = vorhabenBestMatch2
            score = score2
            indexVorh = indexVorh2

        if dtMtSort[indexVorh][1] < 90:
            score -= 4
        elif dtMtSort[indexVorh][1] < 365:
            score -= 2

    else:
        if (wtMtSort[0][0] == obMtSort[0][0]) and (wtMtSort[0][0] != "noMatch"):
            vorhabenBestMatch = wtMtSort[0][0]
            score -= 3
        elif wtMtSort[0][1] > obMtSort[0][1]:
            vorhabenBestMatch = wtMtSort[0][0]
        else:
            vorhabenBestMatch = obMtSort[0][0]

    if adMt:
        score -= 2

    if len(list(set(moeglVorhList))) == 1:
        if score > 6:
            score = 6

    if score > 6:
        if not dtMtSort:
            dtMtSort = [['noMatch', 0]]
        # Konfidenz in Vorhaben-Treffer nicht ausreichend
        wtMtTitleNoMatch = [item[0] for item in wtMtSort]
        obMtTitleNoMatch = [item[0] for item in obMtSort]
        dtMtTitleNoMatch = [item[0] for item in dtMtSort]

        obMtTitleNoMatch.extend(wtMtTitleNoMatch)
        dtMtTitleNoMatch.extend(obMtTitleNoMatch)
        vorhabenBestMatch = list(set(dtMtTitleNoMatch))

    if type(vorhabenBestMatch) is not list:
        vorhabenBestMatch = [vorhabenBestMatch]

    if 'noMatch' in vorhabenBestMatch:
        vorhabenBestMatch.remove('noMatch')

    if not vorhabenBestMatch:
        vorhabenBestMatch = list(set(moeglVorhList))
        score = 9999

    return vorhabenBestMatch, score


def getVorhabenMatches(inhalt, vorhOntol, allVorhDict, moeglOrt, adressenDict, datenDatei):
    adMt = []
    dtMt = []
    wtMt = []
    obMt = []

    preprocInhalt, [], [] = extractText.preprocessText(inhalt)
    preprocInhalt = list(set(preprocInhalt))
    preprocInhalt = getVorhaben.entfernenWennFürVorhabenGleichhueltig(preprocInhalt)

    preprocInhaltOb = []
    for item in preprocInhalt:
        if item in vorhOntol['words'].keys():
            preprocInhaltOb.extend(vorhOntol['words'][item])
    preprocInhaltOb = list(set(preprocInhaltOb))

    minDeltaTime = abs(datetime.timedelta(days=365 * 5).days)
    minDeltaTimeBetter = abs(datetime.timedelta(days=365 * 1.5).days)
    vorhMinDeltaTime = []
    maxPercMatch = 0
    maxPercMatchOb = 0

    for ortMoeg in moeglOrt:
        if ortMoeg in adressenDict.keys():
            adMt.append(ortMoeg)

    for key in allVorhDict.keys():

        for innerkey in allVorhDict[key].keys():

            for vorhkey in allVorhDict[key][innerkey]['vorhaben'].keys():

                # Datumvergleich
                if allVorhDict[key][innerkey]['vorhaben'][vorhkey]['datum']:
                    if type(allVorhDict[key][innerkey]['vorhaben'][vorhkey]['datum'][0]) == str:
                        tempTime = helpers.convertstring2date(
                            allVorhDict[key][innerkey]['vorhaben'][vorhkey]['datum'][0])
                    else:
                        tempTime = allVorhDict[key][innerkey]['vorhaben'][vorhkey]['datum'][0]

                    deltaTimeFileVorh = abs((datenDatei - tempTime).days)

                    if deltaTimeFileVorh < minDeltaTimeBetter:
                        minDeltaTime = deltaTimeFileVorh
                        dtMt.append([vorhkey, deltaTimeFileVorh])
                    elif deltaTimeFileVorh < minDeltaTime:
                        dtMt.append([vorhkey, deltaTimeFileVorh])

                # Wortevergleich
                vorhpp = allVorhDict[key][innerkey]['vorhaben'][vorhkey]['preproc']
                if vorhpp:
                    percentMatch = getVorhaben.matchVorhaben(preprocInhalt, vorhpp)

                    if percentMatch > maxPercMatch:
                        maxPercMatch = percentMatch
                        vorhMaxPercMatch = vorhkey
                        wtMt.append([vorhMaxPercMatch, maxPercMatch])

                # Oberbegriffenvergleich
                vorhob = allVorhDict[key][innerkey]['vorhaben'][vorhkey]['oberbegriffe']
                if vorhob:
                    percentMatchOb = getVorhaben.matchVorhaben(preprocInhaltOb, vorhob)

                    if percentMatchOb > maxPercMatchOb:
                        maxPercMatchOb = percentMatchOb
                        vorhMaxPercMatchOb = vorhkey
                        obMt.append([vorhMaxPercMatchOb, maxPercMatchOb])

    dtMtSort = sorted(dtMt, key=itemgetter(1))
    wtMtSort = sorted(wtMt, key=itemgetter(1))
    obMtSort = sorted(obMt, key=itemgetter(1))

    return dtMtSort, wtMtSort, obMtSort, adMt


def saveVorhaben(dateiname, pfad, allVorhDic):
    outputDir = sys.path[0] + '\\extractMetadata\\outputResult\\'
    outputFilename = 'vorhabenTreffer'
    dictToSave = {pfad: {dateiname: allVorhDic}}
    helpers.save(pfad, outputFilename, dictToSave, outputDir)


def saveVorhabenText(stringTextFile, dateiname, pfad):
    outputDir = sys.path[0] + '\\extractMetadata\\outputResult\\'
    helpers.writeFile(dateiname, pfad, stringTextFile, outputDir)
