#!/usr/bin/env python
# coding: utf-8

import difflib
import re
import pandas as pd
from ast import literal_eval

import Misc.helpers as helpers
import extract.extractAdresse as extractAdresse
import Misc.schluesselregex as rex



def getObjnr(adressen, inhaltDatei):
    
    behoerdenDict = extractAdresse.getBehoerde()    
    hidaTabelle = pd.read_csv(r'Dictionaries\hidaData.csv', sep='\t', encoding='utf-8', usecols=['denkmalStrasse', 'denkmalHausnr', 'denkmaleObjNr', \
                                                                                   'denkmaleAdresse', 'denkmalSachbegriff', 'denkmalName'])
    strassenListe = hidaTabelle['denkmalStrasse'].tolist()
    hnrListe = hidaTabelle['denkmalHausnr'].tolist()
    objnrListe = hidaTabelle['denkmaleObjNr'].tolist()
    adresseListe = hidaTabelle['denkmaleAdresse'].tolist()
    denkmalSachbegriff = hidaTabelle['denkmalSachbegriff'].tolist()
    denkmalName = hidaTabelle['denkmalName'].tolist()
    
    keySummary = {}
    
    methodAll = []
    behList = []
    for key in adressen.keys():
    
        method = []
        objnrHnrList = []      

        key2 = key.replace('strasse','str')
        key3 = key.replace('strasse','straße')
        keyD = []
        if key in strassenListe:
            keyD = key
        elif key2 in strassenListe:
            keyD = key2
        elif key3 in strassenListe:
            keyD = key3
        #TODO: else: suche Abkürzung
        
        for innerKey in adressen[key].keys():

            meth = ''
            #objnrHnrList = []
            
            if keyD:
                # Strasse wurde in denkmalStrasse-Dict gefunden 
                
                indices = [i for i, x in enumerate(strassenListe) if x == keyD]

                # Prüfen of eine Hausnummer vorhanden ist, und ob 
                # es auch dort einen genauen Match gibt
                if adressen[key][innerKey]['hausnummer']:
                    # Hausnummer in der Adresse der Datei vorhanden
                    
                    objnr = []
                    for nr in adressen[key][innerKey]['hausnummer']:

                        hnrD = [hnrListe[iD] for iD in indices]
                        hnrD_indice = [i for i, e in enumerate(hnrD) if e == nr]
                        
                        removeNr, moeglicheBehAdr = isBehoerde(keyD, hnrD, behoerdenDict)
                        
                        if removeNr:
                            # Gefundene Adresse entspricht die einer Behoerde
                            behList.append(moeglicheBehAdr)
                            meth = 'notValid'
                            continue

                        if hnrD_indice:
                            indices_match = [indices[iDm] for iDm in hnrD_indice]
                            objnr = [objnrListe[iD] for iD in indices_match]
                            meth = ['exact_match_adresse']*len(objnr)

                            objnrHnrList.extend(objnr)
                            method.extend(meth)

                            
                if meth == '':
                    # keine übereinstimmende Hausnummer gefunden
                    # Mögliche trifftige Objektnummer werden aufgelistet
                    objnr = [objnrListe[iD] for iD in indices]
                    sachb = [denkmalSachbegriff[iD] for iD in indices]
                    denkname = [denkmalName[iD] for iD in indices]
                    
                    listObjnrGlaubwuerdig = pruefenGlaubwuerdigkeitInMethod(inhaltDatei, objnr, sachb, denkname)
                    
                    meth = ['exact_match_strasse']*len(listObjnrGlaubwuerdig)
                    objnrHnrList.extend(listObjnrGlaubwuerdig)
                    method.extend(meth)
                        

            else:
                # Strasse wurde nicht in denkmalStrasse-Dict gefunden (unkorrigierter Typo?) --> closest match wird gesucht
                
                objnr = []
                
                if adressen[key][innerKey]['hausnummer']:
                    # Hausnummer vorhanden
                    for nr in adressen[key][innerKey]['hausnummer']:
                        
                        # Strasse wurde nicht in denkmalStrasse-Dict gefunden
                        adr = key + ' ' + nr
                        matchPfad = difflib.get_close_matches(adr, adresseListe, n=1, cutoff = 0.8)

                        if matchPfad:
                            objnr = [objnrListe[adresseListe.index(matchPfad[0])]]   
                            sachb = [denkmalSachbegriff[adresseListe.index(matchPfad[0])]]   
                            denkname = [denkmalName[adresseListe.index(matchPfad[0])]]  
                            
                            listObjnrGlaubwuerdig = pruefenGlaubwuerdigkeitInMethod(inhaltDatei, objnr, sachb, denkname)
                                                        
                            meth = ['closest_match']*len(listObjnrGlaubwuerdig)
                            
                            objnrHnrList.extend(listObjnrGlaubwuerdig)
                            method.extend(meth)  
        
        # Objektnr. nach Methoden zusammenfassen
        methodDict = {'exact_match_adresse': [], 'exact_match_strasse': [], 'closest_match': []}
        dummyDict = {'exact_match_adresse': [], 'exact_match_strasse': [], 'closest_match': []}
        
        for elem in range(0,len(method)):
            onr = objnrHnrList[elem][:10]
            if onr not in dummyDict[method[elem]]:
                dummyDict[method[elem]].append(onr)
                
                if onr in objnrListe:
                    methodDict[method[elem]].append([onr])                    
            
        dictEintrag = {'treffer': methodDict, 'hausnummer': adressen[key][innerKey]['hausnummer']}
        
        keySummary[key] = dictEintrag
        methodAll.extend(method)
        
    XX, acceptedMethod, acceptedObjnr = summaryVerfeinern(keySummary, methodAll)    
    objnr = list(set([item for sublist in acceptedObjnr for item in sublist]))               
    
    return objnr, behList, acceptedMethod

def getObjnrAdresse(adressenPfad, strassenListe, adresseListe, hnrListe, objnrListe, sachbegriffListe, denkmalnameListe, behoerdenDict):
    # print(adressenPfad)
    
    keySummary = {}
    
    # adressenPfad = {'Akazhof': {'hausnr' : [1, 15]}, 'Falkenberg': {'hausnr' : [none]}}
    # key: 'Akazhof'
    # innerKey: 15
    
    methodAll = []
    behList = []
    for key in adressenPfad.keys():
    
        method = []
        objnrHnrList = []      

        key2 = key.replace('strasse','str')
        key3 = key.replace('strasse','straße')
        keyD = []
        if key in strassenListe:
            keyD = key
        elif key2 in strassenListe:
            keyD = key2
        elif key3 in strassenListe:
            keyD = key3
        #TODO: else: suche Abkürzung
        
        for innerKey in adressenPfad[key].keys():

            meth = ''
            #objnrHnrList = []
            
            if keyD:
                # Strasse wurde in denkmalStrasse-Dict gefunden 
                
                indices = [i for i, x in enumerate(strassenListe) if x == keyD]

                # Prüfen of eine Hausnummer vorhanden ist, und ob 
                # es auch dort einen genauen Match gibt
                if adressenPfad[key][innerKey]['hausnummer']:
                    # Hausnummer in der Adresse der Datei vorhanden
                    
                    objnr = []
                    for nr in adressenPfad[key][innerKey]['hausnummer']:

                        hnrD = [hnrListe[iD] for iD in indices]
                        hnrD_indice = [i for i, e in enumerate(hnrD) if e == nr]
                        
                        removeNr, moeglicheBehAdr = isBehoerde(keyD, hnrD, behoerdenDict)
                        
                        if removeNr:
                            # Gefundene Adresse entspricht die einer Behoerde
                            behList.append(moeglicheBehAdr)
                            meth = 'notValid'
                            continue

                        if hnrD_indice:
                            indices_match = [indices[iDm] for iDm in hnrD_indice]
                            objnr = [objnrListe[iD] for iD in indices_match]
                            meth = ['exact_match_adresse']*len(objnr)

                            objnrHnrList.extend(objnr)
                            method.extend(meth)

                            
                if meth == '':
                    # keine übereinstimmende Hausnummer gefunden
                    # Mögliche trifftige Objektnummer werden aufgelistet
                    objnr = [objnrListe[iD] for iD in indices]
                    meth = ['exact_match_strasse']*len(objnr)

                    objnrHnrList.extend(objnr)
                    method.extend(meth)
                        

            else:
                # Strasse wurde nicht in denkmalStrasse-Dict gefunden (unkorrigierter Typo?) --> closest match wird gesucht
                
                objnr = []
                
                if adressenPfad[key][innerKey]['hausnummer']:
                    # Hausnummer vorhanden
                    for nr in adressenPfad[key][innerKey]['hausnummer']:
                        
                        # Strasse wurde nicht in denkmalStrasse-Dict gefunden
                        adr = key + ' ' + nr
                        matchPfad = difflib.get_close_matches(adr, adresseListe, n=1, cutoff = 0.8)

                        if matchPfad:
                            objnr = [objnrListe[adresseListe.index(matchPfad[0])]]                            
                            meth = ['closest_match']*len(objnr)
                            
                            objnrHnrList.extend(objnr)
                            method.extend(meth)  
                    
        
        # Objektnr. nach Methoden zusammenfassen
        methodDict = {'exact_match_adresse': [], 'exact_match_strasse': [], 'closest_match': []}
        dummyDict = {'exact_match_adresse': [], 'exact_match_strasse': [], 'closest_match': []}
        
        for elem in range(0,len(method)):
            onr = objnrHnrList[elem][:10]
            if onr not in dummyDict[method[elem]]:
                dummyDict[method[elem]].append(onr)
                
                if onr in objnrListe:
                    methodDict[method[elem]].append([onr, sachbegriffListe[objnrListe.index(onr)], denkmalnameListe[objnrListe.index(onr)]])                    
            
        dictEintrag = {'treffer': methodDict, 'hausnummer': adressenPfad[key][innerKey]['hausnummer']}
        
        keySummary[key] = dictEintrag
        methodAll.extend(method)
        
    keySummaryVerfeinert, acceptedMethod, [] = summaryVerfeinern(keySummary, methodAll)
        
    keySummaryVerfeinert['behoerde'] = behList
    keySummaryVerfeinert['method'] = acceptedMethod

    return keySummaryVerfeinert



def isBehoerde(strname, nrs, behoerdenDict): 
    
    behCheckList = []
    
    for nr in nrs:
        behCheck = strname + ' ' + nr
        match_behoerde = difflib.get_close_matches(behCheck, behoerdenDict.values(), n=1, cutoff = 0.8)

        removeNr = False
        if match_behoerde:
            # TODO: Wenn die Adresse zu einer Denkmalbehörde gehört, wird diese unter "behoerde" aufgelistet.
            # Die Behoerdenadresse wird dann auch aus der Liste der Adressen gelöscht. Dieser Ansatz muss
            # eventuell verfeinert werden: es kann sein, dass die Behoerdenadresse tatsächlich das Denkmal
            # ist, an dem bauliche Maßnahmen durchgeführt werden sollen.
            removeNr = True
            behCheckList.append(match_behoerde[0])
    
    behCheckList = list(set(behCheckList))
    return removeNr, behCheckList


def summaryVerfeinern(summaryDict, methodAll):
    setOfMethods = list(set(methodAll))
    
    acceptedEntries = ''    
    if 'exact_match_adresse' in setOfMethods:
        acceptedEntries = 'exact_match_adresse'
    elif 'exact_match_strasse' in setOfMethods:
        acceptedEntries = 'exact_match_strasse'
    elif 'closest_match' in setOfMethods:
        acceptedEntries = 'closest_match'
        
    keystopop = []
    validObjnr = []
    if acceptedEntries == '':
        keySummaryExklusiver = {}
    else:
        for entrykey in summaryDict:
            if summaryDict[entrykey]['treffer'][acceptedEntries] == []:
                keystopop.append(entrykey)
            else:
                for methodKey in summaryDict[entrykey]['treffer'].keys():
                    if methodKey != acceptedEntries:
                        summaryDict[entrykey]['treffer'][methodKey] = []
                    else:
                        validObjnr.extend(summaryDict[entrykey]['treffer'][methodKey])
    
        keySummaryExklusiver = summaryDict
        for keytopop in keystopop:
            keySummaryExklusiver.pop(keytopop)
            
    return keySummaryExklusiver, acceptedEntries, validObjnr



def getObjNrAusPfad(root, files, denkmalStrasse, denkmaleAdresse, denkmalHausnr, denkmaleObjNr, denkmalSachbegriff, denkmalName, typoSpellcheck, behoerdenDict):
    
    folderDict = {}
    exceptions = 0
    
    pfadString = re.sub("[a-zA-Z äÄöÖüÜß]+", lambda ele: " " + ele[0] + " ", root)
    pfadString = pfadString.replace('\ ', '').replace('_', ' ')    
        
    adressenAusPfad, adresse, adrName = extractAdresse.getAdresse(pfadString, typoSpellcheck)   

    summaryDict = {}
    
    if adressenAusPfad:
        
        summaryDict = getObjnrAdresse(adressenAusPfad, denkmalStrasse, denkmaleAdresse, denkmalHausnr, denkmaleObjNr, denkmalSachbegriff, denkmalName, behoerdenDict)
        
    if (summaryDict) and ('exact_match_adresse' in summaryDict['method']):
        # Adresse wurde exact gefunden. Es wird davon ausgegangen, dass alle Dateien in dem Ordner zu dieser Adresse gehören
        folderDict['pfadtreffer'] = summaryDict
        folderDict['dateien'] = files  
        
    else:
        # kein Exakter Adressenmatch im Pfad
        folderDict['pfadtreffer'] = {} 
        folderDict['dateien'] = {}

    return folderDict



def getObjnrDirekt(inhalt, denkmale, zaehler, foundObjnr):
    
    resultDict = {} 
    
    objnr_aus_datei = rex.getRegex(inhalt).objnr

    if objnr_aus_datei:
        zaehler += 1
        foundObjnr = True
        methodInhalt = 'inhalt_direct'

        if len(objnr_aus_datei) == 1:
            final_objnr = [objnr_aus_datei[0]]
        else:
            final_objnr = [helpers.most_frequent(objnr_aus_datei)]


        objDemo = list(final_objnr)                     
        nameDemoD =[]
        sachDemoD = []
        for demoitemI in range(0,len(objDemo)):
            demoitem = objDemo[demoitemI]
            if demoitem not in denkmale.keys():
                demoitem +=',T'
            if demoitem in denkmale.keys():
                if denkmale[demoitem]['Denkmalname']:
                    nameDemoD.append(denkmale[demoitem]['Denkmalname'])
                if denkmale[demoitem]['Sachbegriff']:
                    sachDemoD.append(denkmale[demoitem]['Sachbegriff'])
                objDemo[demoitemI] = demoitem

        resultDict = {'treffer': {methodInhalt : [objDemo, sachDemoD, nameDemoD]}, 'hausnummer': 'notInquired', 'behoerde': [], 'method': methodInhalt}         
        
    return resultDict, foundObjnr, zaehler


def pruefenObExakt(dictDatei, zaehler, foundObjnr):
    if (dictDatei) and ('exact_match_adresse' in dictDatei['method']):
        # Datei hat mindestens eine zuverlässige Objektnummer, die mit Straßenname + Hausnummer identifiziert wurde. 
        # Nur noch das Vorhaben für diese Datei muss noch bestimmt werden

        for key in dictDatei:
            if key not in ['behoerde', 'method']:
                if (dictDatei[key]['treffer']['exact_match_adresse']):
                    dictDatei[key]['treffer']['exact_match_strasse'] = [] # wird zurückgesetzt, weil es verhältnismäßig ungenau ist
                    dictDatei[key]['treffer']['closest_match'] = [] # wird zurückgesetzt, weil es verhältnismäßig ungenau ist
                    
        zaehler += 1
        foundObjnr = True

    return dictDatei, zaehler, foundObjnr
    
    
def pruefenObBehoerde(dictResult, key, behoerdenDict):
    if (dictResult[key]['treffer']['exact_match_adresse']):
        # Check ob Adressenmatch sich auf eine Behoerde bezieht
        for ihnr in dictResult[key]['hausnummer']:
            behCheck = key + ' ' + ihnr

            match_behoerde = difflib.get_close_matches(behCheck, behoerdenDict.values(), n=1, cutoff = 0.8)

            if match_behoerde:
                # TODO: Wenn die Adresse zu einer Denkmalbehörde gehört, wird diese unter "behoerde" aufgelistet.
                # Die Behoerdenadresse wird dann auch aus der Liste der Adressen gelöscht. Dieser Ansatz muss
                # eventuell verfeinert werden: es kann sein, dass die Behoerdenadresse tatsächlich das Denkmal
                # ist, an dem bauliche Maßnahmen durchgeführt werden sollen.
                dictResult[key]['hausnummer'].remove(ihnr)

                if (dictResult[key]['hausnummer'] == []) and (dictResult[key]['treffer']['exact_match_adresse']):
                    dictResult[key]['treffer']['exact_match_adresse'] = []

                dictResult['behoerde'].append(behCheck)

    return dictResult



def pruefenGlaubwuerdigkeit(dictResult, key, matchType, inhaltDatei, foundObjnr):

    abkrz = dictResult[key]['treffer'][matchType]

    toRemove = []
    for istrmatch in range(0,len(abkrz)):

        moeglicheSchluesselworte = abkrz[istrmatch][1][:] + abkrz[istrmatch][2][:]

        if any(itemSB in inhaltDatei for itemSB in moeglicheSchluesselworte):
            foundObjnr = True                                    

        else:
            toRemove.append(abkrz[istrmatch])

    [dictResult[key]['treffer'][matchType].remove(itoRemove) for itoRemove in toRemove]
    
    keepKey = False
    for methodKey in dictResult[key]['treffer'].keys():
         if dictResult[key]['treffer'][methodKey] != []:
            keepKey = True
    
    return dictResult, foundObjnr, keepKey


def pruefenGlaubwuerdigkeitInMethod(inhaltDatei, foundObjnr, sachbegriff, denkmalname):
    
    listObjnrGlaubwuerdig = []
    for i in range(0,len(foundObjnr)):
        moeglicheSchluesselworte = literal_eval(sachbegriff[i]) + literal_eval(denkmalname[i])
        
        if any(itemSB in inhaltDatei for itemSB in moeglicheSchluesselworte):
            listObjnrGlaubwuerdig.append(foundObjnr[i])
            
    return listObjnrGlaubwuerdig