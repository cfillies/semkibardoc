from typing import List, Dict, Set
from pymongo.collection import Collection

import re
from spellchecker import SpellChecker
from metadata.extractAddress import getAddress, getSpellcheck


def matchingMonuments(adrdict: Dict, slist: List[str], hidacache: Dict[str, str]) -> Set[any]:
    res = set([])
    # fnd = False
    for k in adrdict.keys():
        if k == None:
            continue
        key2 = k.replace('strasse', 'str')
        key3 = k.replace('strasse', 'straße')
        keyD = k
        if k in slist:
            keyD = k
        elif key2 in slist:
            keyD = key2
        elif key3 in slist:
            keyD = key3
        if not keyD in slist:
            continue
            # print("not a hida street:", keyD)
        else:
            # slist.append(keyD)
            x = adrdict[k]
            # adict2[keyD] = adrdict[k]
            snums = x[next(iter(x))]["hausnummer"]
            for hn in snums:
                a = keyD + " " + hn
                if a in hidacache:
                    id = hidacache[a]
                    res.add(id)
                    fnd = True
    # if not fnd and len(adrdict.keys())>0:
    #     print("No matching Address: ", adrdict)
    return res


def getMonumentByAddress(doc: Dict, allstreets: List[str], authoritylist: List[str], hidacache):
    if 'adrDict' in doc:
        adressen = doc['adrDict']
        monu = list(matchingMonuments(adressen, allstreets, hidacache))
        if len(monu) > 0 and monu[0] != '09095169':
            print("Address: ", doc["file"], monu)
        # else:
        #     print(doc["file"])
        return monu
    return []


def getMonumentByFile(doc: Dict, allstreets: List[str], authoritylist: List[str],
                      hidacache: Dict[str, str], sp: SpellChecker, adcache) -> List[Dict]:
    if 'file' in doc:
        filestr = re.sub("[a-zA-Z äÄöÖüÜß]+",
                         lambda ele: " " + ele[0] + " ", doc["file"])
        filestr = filestr.replace('\ ', '').replace('_', ' ')
        adressen, adresse, adrName = getAddress(
            filestr, sp, adcache, allstreets, [], [])
        if len(adressen) == 0:
            return []
        monu: List(Dict) = list(matchingMonuments(adressen, allstreets, hidacache))
        if len(monu) > 0 and monu[0] != '09095169':
            print("Filename: ", doc["file"], monu)
        # else:
        #     print(doc["file"])
        return monu
    return []


def getMonumentByFolder(doc: Dict, allstreets: List[str], authoritylist: List[str],
                        hidacache: Dict[str, str], sp: SpellChecker, adcache) -> List[Dict]:
    if 'path' in doc:
        pathstr = re.sub("[a-zA-Z äÄöÖüÜß]+",
                         lambda ele: " " + ele[0] + " ", doc["path"])
        pathstr = pathstr.replace('\ ', '').replace('_', ' ')
        pathstr = pathstr.replace('\\', ' ')
        adressen, adresse, adrName = getAddress(
            pathstr, sp, adcache, allstreets, [], [])
        if len(adressen) == 0:
            return []
        monu: List(Dict) = list(matchingMonuments(adressen, allstreets, hidacache))
        if len(monu) > 0 and monu[0] != '09095169':
            print("Foldername: ", doc["file"], doc["path"], monu)
        # else:
        #     print(doc["file"])
        return monu
    return []


def findMonuments(col: Collection, hidaname: str, supcol: Collection, lan: str):
    sup: Dict = supcol.find_one()
    alist: List[str] = sup["authorities"]
    slist: List[str] = [x.lower() for x in sup["streetnames"]]

    hidacache = indexMonuments(hidaname)

    # changes = []
    dlist = []
    for doc in col.find():
        dlist.append(doc)
    i = 0

    sp = getSpellcheck(lan, slist)
    dlist = []
    for doc in col.find():
        dlist.append(doc)
    adcache = {}
    for doc in dlist:
        i = i + 1
        if i > 0:
            objID = getMonumentByAddress(
                doc, slist, alist, hidacache)
            if len(objID) == 0:
                objID = getMonumentByFolder(
                    doc, slist, alist, hidacache, sp, adcache)
            if len(objID) == 0:
                objID = getMonumentByFile(
                    doc, slist, alist, hidacache, sp, adcache)
            if len(objID) > 0:
                col.update_one({"_id": doc["_id"]}, {"$set": {"hidas": objID}})
            else:
                col.update_one({"_id": doc["_id"]}, {"$unset": {"hidas": 1}})

            # if len(objID) == 0:
            #     print(doc["file"])


def indexMonuments(col: Collection) -> Dict[str, str]:
    # sup: Dict = supcol.find_one()
    # alist: List[str] = sup["authorities"]
    # slist: List[str] = sup["streetnames"]

    # changes = []
    dlist = []
    for doc in col.find():
        dlist.append(doc)
    i = 0
    hidacache = {}
    for doc in dlist:
        i = i + 1
        if i > 0:
            if "AdresseDict" in doc:
                id_ = ""
                if "OBJ-Dok-Nr" in doc:
                    id_ = doc["OBJ-Dok-Nr"]
                else:
                    if "Teil-Obj-Dok-Nr" in doc:
                        id_ = doc["Teil-Obj-Dok-Nr"][0]
                if not id_ == "":
                    hida_dict = doc["AdresseDict"]
                    for hida_str in hida_dict.keys():
                        hl = hida_str.lower()
                        for hida_num in hida_dict[hida_str]:
                            hidacache[hl + " " + hida_num] = id_
    return hidacache
