# https://pyspellchecker.readthedocs.io/en/latest/
# https://github.com/barrust/pyspellchecker
from typing import List, Dict
from spellchecker import SpellChecker
import re
import numpy as np
import schluesselregex as rex
# import pymongo
from pymongo.collection import Collection



def getSpellcheck(lan: str, words: List[str]) -> SpellChecker:
    sp = SpellChecker(language=lan, distance=1)
    sp.word_frequency.load_words(words)
    return sp

typocache = {}

def corrAdresseTypo(strName: str, typoSpellcheck: SpellChecker):
        if strName in typocache:
            return typocache[strName]
        else:
            if typoSpellcheck.unknown([strName]):
                x = typoSpellcheck.correction(strName)
                if not x == strName:
                    print("Fixed:",x,strName)
                typocache[strName]= x
                return x
        # print(adrCorr + ' --> ' + corr)
        # print('alle Möglichkeiten:' + str(deutsch.candidates(word)))
        return strName


def getAddress(textRaw: str, typoSpellcheck: SpellChecker, adcache: any, streets: List[str]):

    textString: str = re.sub(
        "[a-zA-Z äÄöÖüÜß]+", lambda ele: " " + ele[0] + " ", textRaw)
    text: str = textString.replace(
        '\\', ' ').replace('\ ', '').replace('_', ' ')

    # typoSpellcheck: SpellChecker = getSpellcheck()

    text_split = text.split()
    text_corr = []
    for word in text_split:
        text_corr.append(
            re.sub('str$|str.$|straße$|staße$|stasse$', 'strasse', word).lower())

    text = ' '.join(text_corr)

    text = text.replace('.', ' ').lower()
    trex = rex.getRegex(text)
    adrName = trex.adresseUnvollstaendig
    adresse = trex.adresse

    adressen = {}

    if (type(adresse) is list) and (adresse):
        for adr in adresse:
            try:
                # TODO: "/" und "-" haben in der Adressenangabe unterschiedliche Bedeutungen. In diesem Skript
                # wird das aber noch nicht berücktichtigt
                adr = adr.replace('/', '-')
                strassenNameOrig = re.findall(
                    '([a-zA-Z äÄöÖüÜß-]*)\d*.*', adr)[0].rstrip()

                streetname = re.sub(
                    'str$|str.$|straße$|staße$|stasse$', 'strasse', strassenNameOrig)
                hausNummer = adr.replace(strassenNameOrig, '').replace(
                    ' ', '').replace('.', ' ').lstrip()

                if not streetname in streets:
                    if streetname.replace('trasse', 'traße') in streets:
                        streetname=streetname.replace('trasse', 'traße')
                    elif streetname.replace('traße', 'trasse') in streets:
                        streetname=streetname.replace('traße', 'trasse')                   
                    else:
                        if streetname in adcache:
                            streetname= adcache[streetname]
                        else:
                            nstrassenName = corrAdresseTypo(streetname, typoSpellcheck)
                            if nstrassenName != streetname:
                                    print(streetname,"->", nstrassenName)
                            nstrassenName=streetname
                            adcache[streetname] = nstrassenName
                            streetname = nstrassenName

                if re.search(r'-\d{1,3}$', hausNummer):
                    # Adresse beinhaltet mehrere Hausnummer: deshalb range aufsplitten und auflisten
                    hausNummerRange = hausNummer.rsplit(
                        ' ', 1)[-1].rsplit('-', 1)

                    if int(hausNummerRange[1])-int(hausNummerRange[0]) > 0:
                        nr_range = np.arange(int(hausNummerRange[0]), int(
                            hausNummerRange[1])+2)  # WARNINg: +1 probably right
                        hausNummer = [item for item in nr_range.astype(str)]

                elif '-' in hausNummer:
                    indStrich = hausNummer.find('-')
                    hausNummerRange = [hausNummer[:indStrich], re.findall(
                        r'\d+', hausNummer[indStrich+1:])[0]]

                    if int(hausNummerRange[1])-int(hausNummerRange[0]) > 0:
                        nr_range = np.arange(int(hausNummerRange[0]), int(
                            hausNummerRange[1])+2)  # WARNINg: +1 probably right
                        hausNummer = [item for item in nr_range.astype(str)]

                hausNummerList = [hausNummer] if isinstance(
                    hausNummer, str) else hausNummer
                hausNummerStr = ''.join(hausNummerList)
                if (streetname in adressen) and (hausNummerStr in adressen[streetname]):
                    adressen[streetname][hausNummerStr]['hausnummer'].extend(
                        hausNummerList)
                else:
                    adressen[streetname] = {
                        hausNummerStr: {'hausnummer': hausNummerList}}
            except:
                pass
                dummy = 99999

    elif (type(adrName) is list) and (adrName):
        for adn in adrName:
            if adn not in adressen:
                adressen[adn] = {'none': {'hausnummer': []}}

    for key in adressen.keys():
        for innerKey in adressen[key].keys():
            adressen[key][innerKey]['hausnummer'] = list(
                set(adressen[key][innerKey]['hausnummer']))

    return adressen, adresse, adrName


def findAddresses(col: Collection, supcol: Collection, lan: str):
    sup: Dict = supcol.find_one()
    slist: List[str] = sup["streetnames"]

    slist =[s.lower() for s in slist]

    sp = getSpellcheck(lan, slist)
    # changes = []
    dlist = []
    for doc in col.find():
        dlist.append(doc)
    adcache = sup["adcache"]
    i = 0
    for doc in dlist:
        i = i+1
        if i > 0 and "text" in doc:
            adrDict, adresse, adrName = getAddress(
                doc["text"], sp, adcache, slist)
            if type(adresse) is list:
                # chg = {"doc": doc["_id"],
                #        "adrDict": adrDict, "adresse": adresse}
                print(i, " ", doc["file"], adrDict)
                col.update_one({"_id": doc["_id"]}, {
                               "$set": {"adrDict": adrDict, "adresse": adresse}})
    supcol.update_one({"_id": sup["_id"]}, {"$set": {"adcache": adcache}})
    # for chg in changes:
    #     col.update_one({"_id": chg[doc]}, {"$set": {"adrDict": chg["adrDict"], "adresse": chg["adresse"]}})
