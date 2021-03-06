# https://pyspellchecker.readthedocs.io/en/latest/
# https://github.com/barrust/pyspellchecker
# from typing import List, Dict
from spellchecker import SpellChecker
import re
import numpy as np
import schluesselregex as rex
# import pymongo
from pymongo.collection import Collection
from metadata.support import logEntry
import requests
import json
import os


def getSpellcheck(lan: str, words: list[str]) -> SpellChecker:
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
                logEntry(["Fixed:", x, strName])
            typocache[strName] = x
            return x
    # print(adrCorr + ' --> ' + corr)
    # print('alle Möglichkeiten:' + str(deutsch.candidates(word)))
    return strName


def getAddress(textRaw: str, typoSpellcheck: SpellChecker, adcache: any,
               streets: list[str], newaddr: list[str], igAdr: list[str]):

    textString: str = re.sub(
        "[a-zA-Z äÄöÖüÜß]+", lambda ele: " " + ele[0] + " ", textRaw)
    text: str = textString.replace(
        '\\', ' ').replace('\ ', '').replace('_', ' ')
    # Remove whitespaces around dashes
    text = "-".join(s.strip() for s in text.split("-"))

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

    for s in streets:
        sl = re.findall(s, text)
        for sl1 in sl:
            if not sl1 in adrName:
                f = text.find(sl1)
                f1 = text[f:f+len(sl1)]
                f2 = text[f+len(sl1)+1:f+len(sl1)+6]
                if f2.find(".") > -1:
                    f2 = f2[:f2.find(".")]
                if f2.find(",") > -1:
                    f2 = f2[:f2.find(",")]
                if f2.find(" ") > -1:
                    f2 = f2[:f2.find(" ")]
                if f2.isnumeric():
                    f3 = f1 + " " + f2
                    # if (type(adresse) is list) and (adresse):
                    if not f3 in adresse:
                        adresse.append(f3)
                        newaddr.append(f3)
                        # print(adresse)
    adresse1 = []

    if (type(adresse) is list) and (adresse):
        for adr in adresse:
            # try:
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
                    streetname = streetname.replace('trasse', 'traße')
                elif streetname.replace('traße', 'trasse') in streets:
                    streetname = streetname.replace('traße', 'trasse')
                else:
                    if streetname in adcache:
                        streetname = adcache[streetname]
                    else:
                        nstrassenName = corrAdresseTypo(
                            streetname, typoSpellcheck)
                        if nstrassenName != streetname:
                            logEntry([streetname, "->", nstrassenName])
                            nstrassenName = streetname
                        adcache[streetname] = nstrassenName
                        streetname = nstrassenName
            if not streetname in adresse1:
                if not adr in adresse1:
                    adresse1.append(adr)
                adressen[streetname] = {}
            if not streetname in streets:
                # Wenn eine Strasse nicht in der HIDA Strassenliste ist, sollte sie ignoriert werden
                # print("Ignoring: " + streetname + " " + adr)
                igAdr.append(adr)
            else:
                if re.search(r'-\d{1,3}$', hausNummer):
                    # Adresse beinhaltet mehrere Hausnummer: deshalb range aufsplitten und auflisten
                    hausNummerRange = hausNummer.rsplit(
                        ' ', 1)[-1].rsplit('-', 1)
                    if hausNummerRange[1].isnumeric() and hausNummerRange[0].isnumeric():
                        if int(hausNummerRange[1])-int(hausNummerRange[0]) > 0:
                            nr_range = np.arange(int(hausNummerRange[0]), int(
                                hausNummerRange[1])+2)  # WARNINg: +1 probably right
                            hausNummer = [
                                item for item in nr_range.astype(str)]

                elif '-' in hausNummer:
                    indStrich = hausNummer.find('-')
                    l = re.findall(r'\d+', hausNummer[indStrich+1:])
                    if len(l) > 0:
                        hausNummerRange = [hausNummer[:indStrich], l[0]]
                        if int(hausNummerRange[1])-int(hausNummerRange[0]) > 0:
                            nr_range = np.arange(int(hausNummerRange[0]), int(
                                hausNummerRange[1])+2)  # WARNINg: +1 probably right
                            hausNummer = [
                                item for item in nr_range.astype(str)]
                elif '#' in hausNummer:
                    indStrich = hausNummer.find('#')
                    l = re.findall(r'\d+', hausNummer[indStrich+1:])
                    if len(l) > 0:
                        hausNummerRange = [hausNummer[:indStrich], l[0]]
                        if int(hausNummerRange[1])-int(hausNummerRange[0]) > 0:
                            nr_range = np.arange(int(hausNummerRange[0]), int(
                                hausNummerRange[1])+2)  # WARNINg: +1 probably right
                            hausNummer = [
                                item for item in nr_range.astype(str)]
                hausNummerList = [hausNummer] if isinstance(
                    hausNummer, str) else hausNummer
                hausNummerStr = ''.join(hausNummerList)
                if (streetname in adressen):
                    if (hausNummerStr in adressen[streetname]):
                        adressen[streetname][hausNummerStr]['hausnummer'].extend(
                            hausNummerList)
                    else:
                        adressen[streetname] = {
                            hausNummerStr: {'hausnummer': hausNummerList}}
                # except:
                #     pass
                #     dummy = 99999

    # elif (type(adrName) is list) and (adrName):
    #     for adn in adrName:
    #         if not adn in streets:
    #            if adn not in adressen:
    #             adressen[adn] = {'none': {'hausnummer': []}}

    for key in adressen.keys():
        for innerKey in adressen[key].keys():
            adressen[key][innerKey]['hausnummer'] = list(
                set(adressen[key][innerKey]['hausnummer']))
    # if len(adresse1) > 0:
    #     print(adresse1)
    return adressen, adresse1, []


def findAddresses(col: Collection, supcol: Collection, lan: str, streets: str):
    sup: dict = supcol.find_one()
    slist: list[str] = sup[streets]

    slist = [s.lower() for s in slist]

    sp = getSpellcheck(lan, slist)
    # changes = []
    dlist = []
    nlist = []
    xlist = []
    for doc in col.find():
        dlist.append(doc)
    adcache = sup["adcache"]
    i = 0
    for doc in dlist:
        i = i+1
        if i > 0 and "text" in doc:
            adrDict, adresse, adrName = getAddress(
                doc["text"], sp, adcache, slist, nlist, xlist)
            if not type(adresse) is list:
                adresse = []
            # logEntry(len(nlist))
            # chg = {"doc": doc["_id"],
            #        "adrDict": adrDict, "adresse": adresse}
            # logEntry([ i, " ", doc["file"], adrDict])
            if not logEntry(["Adresse: ", i, " ", doc["file"]]):
                return
            col.update_one({"_id": doc["_id"]}, {
                "$set": {"adrDict": adrDict, "adresse": adresse}})
    supcol.update_one({"_id": sup["_id"]}, {"$set": {"adcache": adcache}})

def exportLocations(col: Collection, pat: Collection):
    # pat.delete_many({})
    for doc in col.find():
        if ("adresse" in doc) and ("location" in doc):
            # adrlist: list = doc["adresse"]
            adrlist = list(map(lambda a: a + " Berlin", doc["adresse"]))
            locs = doc["location"]
            if len(adrlist) > 0 and type(locs) is list:
                if len(adrlist) > 5:
                    adrlist=adrlist[:5]
                zlist = zip(adrlist, locs)
                for z in zlist:
                    adr = z[0]
                    loc = z[1]
                    pat.update_one({"adresse": adr}, { "$set": { "location": loc}}, upsert=True)
                
    
def findLocations(col: Collection):
    dlist = []
    for doc in col.find():
        dlist.append(doc)
    i = 0
    geo_url = "http://localhost:7071/api"
    apikey = os.getenv("LOCATION_API_KEY")

#    for doc in col.find():
    for doc in dlist:
        i = i+1
        if i > 0 and ("adresse" in doc) and not ("location" in doc):
            adrlist: list = doc["adresse"]
            if len(adrlist) > 0:
                if len(adrlist) > 5:
                    adrlist=adrlist[:5]
                alist = list(map(lambda a: a + " Berlin", doc["adresse"]))
                body = {"adress": alist, 
                        "apikey": apikey,
                        "database": "kibardoc",
                        "collection": "location"}
                loc = requests.post(geo_url + "/geocode/forward", json=body,
                                    headers={"Accept": "application/json"})
                js = json.loads(loc.content)
                col.update_one({"_id": doc["_id"]}, {
                    "$set": {"location": js}})
                if not logEntry(["Location: ", i, " ", doc["file"]]):
                    return

def findaLocation(col: Collection):
    dlist = []
    for doc in col.find():
        dlist.append(doc)
    i = 0

#    for doc in col.find():
    for doc in dlist:
        i = i+1
        if i > 0 and ("location" in doc):
            locs = doc["location"]
            if isinstance(locs,list):
                if len(locs) > 0:
                    loc0 = locs[0]
                    if loc0 and "features" in loc0 and len(loc0["features"]) > 0:
                        geo = loc0["features"][0]["geometry"]
                        col.update_one({"_id": doc["_id"]}, {
                            "$set": {"alocation": geo}})
                        if not logEntry(["aLocation: ", i, " ", doc["file"]]):
                            return
            else:
                print(locs)
