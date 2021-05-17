#!/usr/bin/env python
# coding: utf-8

import json
import re
import Misc.schluesselregex as rex
import Misc.helpers as helpers
import numpy as np

#https://pyspellchecker.readthedocs.io/en/latest/
#https://github.com/barrust/pyspellchecker
from spellchecker import SpellChecker


def getAdresse(text, typoSpellcheck):
    
    #text = re.sub(r"([0-9]+(\.[0-9]+)?(\-?)?([0-9]+(\.[0-9]+)?))",r" \1 ", text).strip()
    text_split = text.split()
    text_corr = []
    for word in text_split:
        text_corr.append(re.sub('str$|str.$|straße$|staße$|stasse$', 'strasse', word).lower())

    text = ' '.join(text_corr)

    text = text.replace('.', ' ').lower()
    adrName = rex.getRegex(text).adresseUnvollstaendig
    adresse = rex.getRegex(text).adresse

    adressen = {}

    if adresse:
        for adr in adresse:
            try: 
                ##########################
                # find Hausnummer first considering differen constellation such as 4,10-14,10/14,10\14,10a-17b, 16a/18b ...
                hausNummerList=re.findall('\d+[A-za-z]?[\s]*[^a-zA-Z0-9,/]{0,3}[\s]*[\d]+\d[A-za-z]?|\d+',adr)
                indexRemoveHausNummer=adr.find(hausNummerList[0])
                strassenName=adr[:indexRemoveHausNummer]
                strassenName=' '.join(strassenName.split())
                # if multiple matches# mostly one match
                for i in range(len(hausNummerList)):
                    hausNummerList[i]=hausNummerList[i].lower()
                    if '-' in hausNummerList[i]:
                        hausNummerList[i]=hausNummerList[i].replace('---','-').replace('- -','-').replace('--','-').replace('+',',').replace(' ','')
                    hausNummerList[i]=' '.join(hausNummerList[i].split())
                    hausNummerList[i]=hausNummerList[i].replace(' ',',')
                    if ',' in hausNummerList[i]:
                        hausNummerList.extend(hausNummerList[i].split(','))
                        hausNummerList.remove(hausNummerList[i])
                ##########################
                strassenName = corrAdresseTypo(strassenName, typoSpellcheck)
                #########################
                hausNummerList2=[]
                for hausNummer in hausNummerList:
                    if re.search(r'[-]\d{1,3}', hausNummer) and re.search(r'[a-z]', hausNummer):
                        abc=list('abcdefghijklmnopqrstuvwxyz')
                        findDigit=re.findall('\d+',hausNummer)
                        findLetter=re.findall('[a-z]',hausNummer)
                        if len(list(set(findDigit)))==1 and len(list(set(findLetter)))==2:
                            index1=abc.index(findLetter[0])
                            index2=abc.index(findLetter[1])+1
                            hausNummer2=[findDigit[0]+abc[i] for i in range(index1,index2)]
                        else:
                            findDigitLetter=re.findall('\d+[a-z]',hausNummer) 
                            for remElement in findDigitLetter:
                                hausNummer=hausNummer.replace(remElement,'')
                            findOnlyDigit=re.findall('\d+[^a-z^-]',hausNummer)
                            hausNummer2=list(set(findDigitLetter))
                            hausNummer2.extend(findOnlyDigit)
                        hausNummerList2.extend(hausNummer2)
                    elif re.search(r'-\d{1,3}$', hausNummer):
                        # Adresse beinhaltet mehrere Hausnummer: deshalb range aufsplitten und auflisten
                        hausNummerRange = hausNummer.rsplit(' ', 1)[-1].rsplit('-', 1)
                        if int(hausNummerRange[1])-int(hausNummerRange[0]) > 0:
                            nr_range = np.arange(int(hausNummerRange[0]),int(hausNummerRange[1])+1) 
                            hausNummer2 = [item for item in nr_range.astype(str)]
                            hausNummerList2.extend(hausNummer2)
                            hausNummerList2.remove(hausNummer)
                    elif '-' in hausNummer:
                        indStrich = hausNummer.find('-')
                        hausNummerRange = [hausNummer[:indStrich], re.findall(r'\d+', hausNummer[indStrich+1:])[0]]
                        if int(hausNummerRange[1])-int(hausNummerRange[0]) > 0:
                            nr_range = np.arange(int(hausNummerRange[0]),int(hausNummerRange[1])+1) 
                            hausNummer2 = [item for item in nr_range.astype(str)]
                            hausNummerList2.extend(hausNummer2)
                    else:
                        hausNummerList2.append(hausNummer)
                #???hausNummerList = [hausNummer] if isinstance(hausNummer, str) else hausNummer
                hausNummerStr = ''.join(hausNummerList)
                if (strassenName in adressen) and (hausNummerStr in adressen[strassenName]):
                    adressen[strassenName][hausNummerStr]['hausnummer'].extend(hausNummerList2)
                else:
                    adressen[strassenName] = {hausNummerStr : {'hausnummer': hausNummerList2}}
            except:
                dummy = 99999


    elif adrName:
        for adn in adrName:
            if adn not in adressen:
                    adressen[adn] = {'none' : {'hausnummer': []}}


    for key in adressen.keys():
        for innerKey in adressen[key].keys():
            adressen[key][innerKey]['hausnummer'] = list(set(adressen[key][innerKey]['hausnummer']))

    return adressen, adresse, adrName
    
    

def corrAdresseTypo(strName,typoSpellcheck):
    if typoSpellcheck.unknown([strName]):
        strName = typoSpellcheck.correction(strName)
        #print(adrCorr + ' --> ' + corr)
        #print('alle Möglichkeiten:' + str(deutsch.candidates(word)))
    return strName     


def getAusHida(denkmalDict):    
    with open(denkmalDict) as f:
        denkmale = json.load(f)

    # Denkmalliste mit jeweiligen Adressen versehen
    denkmaleAdresse = list()
    denkmalStrasse = list()
    denkmalHausnr = list()
    denkmalSachbegriff = list()
    denkmaleObjNr = list()
    denkmalName = list()


    for key in denkmale:
        if 'AdresseDict' in denkmale[key].keys():
            adressen=[]
            adressenDict = denkmale[key]['AdresseDict']
            for keyAdr in adressenDict:
                hausnummer = adressenDict[keyAdr]
                if not hausnummer:
                    hausnummer = '99999'

                for hnr in hausnummer:
                    if 'Sachbegriff' in denkmale[key].keys():
                        denkmalSachbegriff.append(denkmale[key]['Sachbegriff'])
                    else:
                        denkmalSachbegriff.append(['none'])

                    if 'Denkmalname' in denkmale[key].keys():
                        denkmalName.append(denkmale[key]['Denkmalname'])
                    else:
                        denkmalName.append(['none'])

                    denkmalStrasse.append(keyAdr.replace("ß", "ss").lower())
                    denkmalHausnr.append(hnr)

                    adr=str(keyAdr.lower()) + ' ' + str(hnr)
                    denkmaleAdresse.append(adr)
                    denkmaleObjNr.append(key)

    # Strassennamen aus Denkmalliste entnehmen und in das Wörterbuch einfügen,
    # um Tippfehler in Adressen korrigieren zu können
    strasseSet = list(set(denkmalStrasse))
    
    return denkmale, denkmaleAdresse, denkmalStrasse, denkmalHausnr, denkmalSachbegriff, denkmaleObjNr, denkmalName, strasseSet

def getBehoerde():
    # Dictionary mit allen Denkmalschutzbehörden erstellen
    # aus:
    # https://www.berlin.de/sen/kulteu/denkmal/organisation-des-denkmalschutzes/untere-denkmalschutzbehoerden/
    # https://www.berlin.de/sen/kulteu/denkmal/organisation-des-denkmalschutzes/landesdenkmalrat/
    # https://www.berlin.de/landesdenkmalamt/

    # Form ist Bezirk:Adresse
    dictBehoerden = {'Charlottenburg-Wilmersdorf': 'Hohenzollerndamm 174',
                 'Friedrichshain-Kreuzberg': 'Yorckstrasse 4',
                 'Lichtenberg':'Alt-Friedrichsfelde 60',
                 'Marzahn-Hellersdorf':'Helene-Weigel-Platz 8',
                 'Mitte':'Müllerstrasse 146',
                 'Neukölln':'Karl-Marx-Strasse 83',
                 'Pankow':'Storkower Strasse 97',
                 'Reinickendorf':'Eichborndamm 215',
                 'Spandau':'Carl-Schurz-Strasse 2',
                 'Steglitz-Zehlendorf':'Kirchstrasse 1',
                 'Tempelhof-Schöneberg':'John-F-Kennedy-Platz',
                 'Treptow-Köpenick':'Alt-Köpenick 21',
                 'Oberste Denkmalschutzbehörde':'Brunnenstrasse 188-190',
                 'Oberste Denkmalschutzbehörde':'Behrenstrasse 42',
                 'Landesdenkmalamt':'Klosterstrasse 47',     
                 'Senatsverwaltung für Stadtentwicklung und Wohnen': 'Württembergische Strasse 6'
                }
    return dictBehoerden



