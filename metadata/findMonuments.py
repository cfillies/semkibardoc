# from typing import List, Dict, Set
from pymongo.collection import Collection

import re
from spellchecker import SpellChecker
from metadata.extractAddress import getAddress, getSpellcheck


def matchingMonuments(adrdict: dict, slist: list[str], hidacache: dict[str, str]) -> set[any]:
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


def getMonumentByAddress(doc: dict, allstreets: list[str], authoritylist: list[str], hidacache):
    if 'adrDict' in doc:
        adressen = doc['adrDict']
        monu = list(matchingMonuments(adressen, allstreets, hidacache))
        if len(monu) > 0 and monu[0] != '09095169':
            print("Address: ", doc["file"], monu)
        # else:
        #     print(doc["file"])
        return monu
    return []


def getMonumentByFile(doc: dict, allstreets: list[str], authoritylist: list[str], hidacache: dict[str, str], hidanamecache: dict[str, str], sp: SpellChecker, adcache) -> list[dict]:
    if 'file' in doc:
        filestr = re.sub("[a-zA-Z äÄöÖüÜß]+",
                         lambda ele: " " + ele[0] + " ", doc["file"])
        filestr = filestr.replace('\ ', '').replace('_', ' ')
        adressen, adresse, adrName = getAddress(
            filestr, sp, adcache, allstreets, [], [])
        monu: list(str)=[]
        if len(adressen)> 0:
            monu = list(matchingMonuments(
                adressen, allstreets, hidacache))
        if monu == []:
            #  ps = filestr.split(" ")
            ps = filestr.lower()
            for mname in hidacache:
                if ps.find(mname)>-1:
                    # res = 3
                    # name += 1
                    monu.append(hidacache[mname])
        if monu == []:
            #  ps = filestr.split(" ")
            ps = filestr
            for mname in hidanamecache:
                 if ps.find(mname)>-1:
                    # res = 3
                    # name += 1
                    monu.extend(hidanamecache[mname])
                    print("MonumentName in File: " + mname + " in " + filestr)

        if len(monu) > 0 and monu[0] != '09095169':
            print("Filename: ", doc["file"], monu)
        # else:
        #     print(doc["file"])
        return monu
    return []


def folderAddress(folders_col: Collection, hida: Collection, path: str, supcol: Collection, lan: str, district: str, streetnames: str):
    sup: dict = supcol.find_one()
    alist: list[str] = sup["authorities"]
    allstreets: list[str] = [x.lower() for x in sup[streetnames]]
    sp = getSpellcheck(lan, allstreets)
    hidacache = indexMonuments(hida, district, streetnames)
    hidanamecache = indexMonumentNames(hida, district, allstreets)
    hidaids = indexMonumentID(hida, district)
    
    adcache = {}
    good = 0
    halfgood = 0
    bad = 0
    name = 0
    dlist = []
    for doc in folders_col.find():
        dlist.append(doc)
    for folder in dlist:
        if len(folder["files"])==0:
            continue
        dir = folder["dir"]
        dir = dir.replace(path, '')

        if dir == '' or dir == '\\1_Treptow':
            continue

        pathstr = re.sub("[a-zA-Z äÄöÖüÜß]+",
                         lambda ele: " " + ele[0] + " ", dir)
        pathstr = " ".join(dir.split("\\"))
        pathstr = pathstr.replace('_', ' ')
        pathstr = pathstr.replace(',', ' ')
        pathstr = pathstr.replace('.', ' ')
        pathstr = pathstr.replace('#', '-')
        # pathstr = pathstr.replace('\\', ' ')
        
        for hidaid in hidaids:
            if pathstr.find("\\" + hidaid + " ")>-1:
                print("hidaid in path: " + hidaid)

        adressen, adresse, adrName = getAddress(
            pathstr, sp, adcache, allstreets, [], [])
        monu: list(dict) = []
        res = 0
        if adressen == {}:
            res = 0
            # print(dir + ": ", adressen)
        else:
            monu = list(matchingMonuments(
                adressen, allstreets, hidacache))
            if len(monu) > 0 and monu[0] != '09095169':
                res = 1
                # print("Filename: ", dir, monu)
            else:
                res = 2
                # print("No monument: ", dir, adressen)

        if monu == []:
            #  ps = pathstr.split(" ")
            ps = pathstr.lower()
            for mname in hidacache:
                if ps.find(mname)>-1:
                    res = 3
                    name += 1
                    monu.append(hidacache[mname])
        if monu == []:
            #  ps = pathstr.split(" ")
            ps = pathstr
            for mname in hidanamecache:
                if ps.find(mname)>-1:
                    res = 3
                    name += 1
                    monu.extend(hidanamecache[mname])
                    # print("Name: " + mname + " in " + pathstr)
        folders_col.find_one_and_update(
            {"_id": folder["_id"]}, {"$set": {"hidas": monu, "adressen": adressen}})

        if res == 0:
            print("Bad: " + dir)
            bad += 1
        elif res == 1:
            good += 1
        elif res == 2:
            halfgood += 1
        elif res == 3:
            good += 1
        print(dir + " " + str(good) + " / " + str(halfgood) +
              " / " + str(bad) + " / " + str(name))

        # else:
        #     print(doc["file"])

    # dir = dir.replace(path, "")
    # f = file
    # if f.endswith(".doc"):
    #     f = f.replace(".doc", ".docx")
    # if f.endswith(".docx"):
    #     print(dir, f)
    #     resolved_col.update_many(
    #         {"file": f}, {"$set": {"dir": dir}})


def getMonumentByFolder(doc: dict, allstreets: list[str], authoritylist: list[str], hidacache: dict[str, str], sp: SpellChecker, adcache) -> list[dict]:
    if 'path' in doc:
        pathstr = re.sub("[a-zA-Z äÄöÖüÜß]+",
                         lambda ele: " " + ele[0] + " ", doc["path"])
        pathstr = pathstr.replace('\ ', '').replace('_', ' ')
        pathstr = pathstr.replace('\\', ' ')
        adressen, adresse, adrName = getAddress(
            pathstr, sp, adcache, allstreets, [], [])
        if len(adressen) == 0:
            return []
        monu: list(dict) = list(matchingMonuments(
            adressen, allstreets, hidacache))
        if len(monu) > 0 and monu[0] != '09095169':
            print("Foldername: ", doc["file"],  doc["path"], monu)
        # else:
        #     print(doc["file"])
        return monu
    return []


def findMonuments(col: Collection, hidaname: str, supcol: Collection, folders_col: Collection, lan: str, district: str, streetnames: str):
    sup: dict = supcol.find_one()
    alist: list[str] = sup["authorities"]
    slist: list[str] = [x.lower() for x in sup[streetnames]]

    hidacache = indexMonuments(hidaname, district, streetnames)
    hidanamecache = indexMonumentNames(hidaname, district, slist)

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
    x = 0
    for doc in dlist:
        i = i+1
        # if not doc["path"] == "C:\\Data\\test\\KIbarDok\\Treptow\\1_Treptow\\1O-Z\\Richterstr. 6":
        #     continue
        if i > 0:
            objID = getMonumentByAddress(
                doc, slist, alist, hidacache)
            # if doc["path"] == "C:\\Data\\test\\KIbarDok\\Treptow\\1_Treptow\\1O-Z\\Richterstr. 6":
            #     print(doc)
            if len(objID) == 0:
                for folder in folders_col.find({"dir": doc["path"]}):
                    if folder and "hidas" in folder:
                        hidas = folder["hidas"]
                        if len(hidas) > 0:
                            objID = hidas
                            print("Foldername: ", doc["file"],  doc["path"], hidas)
                            x += 1
                            break
            if len(objID) == 0:
                objID = getMonumentByFolder(
                    doc, slist, alist, hidacache, sp, adcache)
            if len(objID) == 0:
                objID = getMonumentByFile(
                    doc, slist, alist, hidacache, hidanamecache, sp, adcache)
            if len(objID) > 0:
                col.update_one({"_id": doc["_id"]}, {"$set": {"hidas": objID}})
            else:
                col.update_one({"_id": doc["_id"]}, {"$unset": {"hidas": 1}})

             # if len(objID) == 0:
            #     print(doc["file"])

    print(x)


def indexMonuments(col: Collection, district: str, streetnames: str) -> dict[str, str]:
    # sup: dict = supcol.find_one()
    # alist: list[str] = sup["authorities"]
    # slist: list[str] = sup[streetnames]

    # changes = []
    dlist = []
    for doc in col.find({"Bezirk": district}):
        dlist.append(doc)
    i = 0
    hidacache = {}
    for doc in dlist:
        i = i+1
        if i > 0:
            if "AdresseDict" in doc:
                id = ""
                if "OBJ-Dok-Nr" in doc:
                    id = doc["OBJ-Dok-Nr"]
                else:
                    if "Teil-Obj-Dok-Nr" in doc:
                        id = doc["Teil-Obj-Dok-Nr"][0]
                if not id == "":
                    hida_dict = doc["AdresseDict"]
                    for hida_str in hida_dict.keys():
                        hl = hida_str.lower().strip()
                        for hida_num in hida_dict[hida_str]:
                            hidacache[hl + " " + hida_num] = id
    return hidacache


def indexMonumentNames(col: Collection, district: str, streets: list[str]) -> dict[str, str]:
    # changes = []
    dlist = []
    for doc in col.find({"Bezirk": district}):
        dlist.append(doc)
    i = 0
    hidanamecache = {}
    for doc in dlist:
        i = i+1
        if i > 0:
            if "OBJ-Dok-Nr" in doc:
                id = doc["OBJ-Dok-Nr"]
                if "Denkmalname" in doc:
                    name = doc["Denkmalname"]
                    for n in name:
                        nl = n.lower().strip()
                        if not nl in streets:
                            if n in hidanamecache:
                                hidanamecache[n].append(id)
                            else:
                                hidanamecache[n] = [id]
    return hidanamecache

def indexMonumentID(col: Collection, district: str) -> list:
    # changes = []
    dlist = []
    for doc in col.find({"Bezirk": district}):
        dlist.append(doc)
    i = 0
    hidaids = []
    for doc in dlist:
        i = i+1
        if i > 0:
            if "OBJ-Dok-Nr" in doc:
                id = doc["OBJ-Dok-Nr"]
                hidaids.append(id)
    return hidaids
