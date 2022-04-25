# import spacy
from numpy import number
import pymongo
import json
import os
# import requests

from pymongo.collection import Collection

import random
# from typing import Dict, Any, List, Tuple
from dotenv import load_dotenv

from metadata.extractText import tikaText
from metadata.support import initSupport, initDocumentPattern
from metadata.extractAddress import findAddresses, findLocations, exportLocations, findaLocation
from metadata.findMonuments import findMonuments, folderAddress
from metadata.findDocType import findDocType
from metadata.extractDocTypeSpacy import findDocTypeSpacy
from metadata.extractDates import findDates
from metadata.extractProject import findProject
from metadata.extractIntents import extractintents, extractTexts
from folders import getFolders

from metadata.support import logEntry, getLog, resetLog, is_cancelled

# from tmtest import tm_test, tm_test2


load_dotenv()

# uri = os.getenv("MONGO_CONNECTION")
uri = "mongodb://localhost:27017"
# uri = os.getenv("MONGO_CONNECTION_ATLAS")
# uri =  os.getenv("MONGO_CONNECTION_KLS")
# uri =  os.getenv("MONGO_CONNECTION_AZURE")
# uri =  os.getenv("MONGO_CONNECTION_KIBARDOC2")
# uri = "mongodb+srv://semtation:SemTalk3!@cluster2.kkbs7.mongodb.net/kibardoc"

myclient = pymongo.MongoClient(uri)
# myclient._topology_settings

mydb = myclient["kibardoc"]
collist = mydb.list_collection_names()


###############################

def cloneCollection(colname: str, desturi: str, destdbname: str, destcolname: str):
    src_col = mydb[colname]
    result = []
    for doc in src_col.find():
        result.append(doc)
    destclient = pymongo.MongoClient(desturi)
    destdb = destclient[destdbname]
    dest_col = destdb[destcolname]
    dest_col.delete_many({})
    dest_col.insert_many(result)

# cloneCollection("metadata", os.getenv("MONGO_CONNECTION_AZURE"), "kibardoc", "metadata")
# cloneCollection("koepnick_folders", os.getenv("MONGO_CONNECTION_AZURE"), "kibardoc", "koepnick_folders")

# cloneCollection("pankow", os.getenv("MONGO_CONNECTION_AZURE"), "kibardoc", "pankow")
# cloneCollection("pankow_folders", os.getenv("MONGO_CONNECTION_AZURE"), "kibardoc", "pankow_folders")
# cloneCollection("metadata", os.getenv("MONGO_CONNECTION"), "kibardoc", "metadata")
# cloneCollection("metadata", "mongodb://localhost:27017", "kibardoc", "metadata")
# cloneCollection("charlottenburg", os.getenv("MONGO_CONNECTION_KLS"), "kibardoc", "charlottenburg")


def cloneDatabase(desturi: str, destdbname: str, badlist: list[str]):
    destclient = pymongo.MongoClient(desturi)
    destdb = destclient[destdbname]
    for colname in collist:
        if colname in badlist:
            continue
        src_col = mydb[colname]
        result = []
        for doc in src_col.find():
            result.append(doc)
        dest_col = destdb[colname]
        dest_col.delete_many({})
        dest_col.insert_many(result)

###############################


def insert_many(items: any, colname: str):
    if len(colname) > 0 and items != {}:
        col: Collection = mydb[colname]
        col.delete_many({})
        col.insert_many(items)


def insert_one(item: any, colname: str):
    if len(colname) > 0 and item != {}:
        col: Collection = mydb[colname]
        col.delete_many({})
        col.insert_one(item)

###############################


def loadArrayCollection(filename: str, colname: str):
    items: any = []
    with open(filename, encoding='utf-8') as f:
        items = json.loads(f.read())
    insert_many(items, colname)


def insertArrayCollection(items: any, colname: str):
    insert_many(items, colname)


def loadDictCollection(filename: str, colname: str):
    item: any = {}
    with open(filename, encoding='utf-8') as f:
        item = json.loads(f.read())
    insert_one(item, colname)


def insertDictCollection(item: any, colname: str):
    insert_one(item, colname)


def patchHida(hida0: dict, hidaname: str):
    monuments = []
    for hid in hida0:
        monument = hida0[hid]
        # if "K-Begründung" in monument:
        #     del monument["K-Begründung"]
        if "AdresseDict" in monument:
            adict = monument["AdresseDict"]
            keys = [x for x in adict]
            for str in keys:
                if "." in str:
                    str2 = str.replace(".", "")
                    adict[str2] = adict[str]
                    del adict[str]
                    continue
        monuments.append(monument)
    hida_col = mydb[hidaname]
    hida_col.delete_many({})
    hida_col.insert_many(monuments)

###############################

# def patchResolved(resolvedname: str, filename: str, hidaname: str):
#     hida_col = mydb[hidaname]
#     resolved_col = mydb[resolvedname]
#     with open(filename, encoding='utf-8') as f:
#         resolvedjs = json.loads(f.read())
#         resolved = []
#         for directory in resolvedjs:
#             el = resolvedjs[directory]
#             if "datei" in el:
#                 filesjs = el["datei"]
#                 for file in filesjs:
#                     # logEntry([directory, file])
#                     obj = filesjs[file]
#                     vorhaben = obj["vorhaben"]
#                     if len(vorhaben) == 1:
#                         if vorhaben[0] == "Errichtung einer Mega-Light-Werbeanlage":
#                             vorhaben = []
#                     vorgang = obj["vorgang"]
#                     objnr = obj["objnr"]
#                     hida = {}
#                     if "method" in objnr:
#                         meth = objnr["method"]
#                         if len(meth) > 0:
#                             for o in objnr:
#                                 if o != "method" and o != "behoerde" and o != "hausnummer":
#                                     if meth == 'inhalt_direct' and o == "treffer":
#                                         treflist = objnr["treffer"][meth]
#                                         tref = treflist[0]
#                                         hidaid = tref[0]
#                                         hidaobj = hida_col.find_one(
#                                             {"OBJ-Dok-Nr": hidaid})
#                                         listentext = hidaobj["Listentext"]
#                                         denkmalname = hidaobj["Denkmalname"]
#                                         denkmalart = hidaobj["Denkmalart"]
#                                         sachbegriff = hidaobj["Sachbegriff"]
#                                         hida[hidaid] = {
#                                             "hidaid": hidaid,
#                                             "Listentext": listentext,
#                                             "Denkmalart": denkmalart,
#                                             "Denkmalname": denkmalname,
#                                             "Sachbegriff": sachbegriff}
#                                         #     if isinstance(hidaobjl, list):
#                                         #         for hidaid in hidaobjl:
#                                         #             hida[hidaid]= { "hidaid": hidaid, "treffer": objnr["treffer"]}
#                                         #     else:
#                                         #             hida[hidaid]= { "hidaid": hidaobjl, "treffer": objnr["treffer"]}
#                                     else:
#                                         denkmal = objnr[o]
#                                         # logEntry(denkmal)
#                                         for hidaobj in denkmal["treffer"][meth]:
#                                             hidaid = hidaobj[0]
#                                             hidaobj = hida_col.find_one(
#                                                 {"OBJ-Dok-Nr": hidaid})
#                                             listentext = hidaobj["Listentext"]
#                                             denkmalname = hidaobj["Denkmalname"]
#                                             denkmalart = hidaobj["Denkmalart"]
#                                             sachbegriff = hidaobj["Sachbegriff"]
#                                             hida[hidaid] = {
#                                                 "hidaid": hidaid,
#                                                 "Listentext": listentext,
#                                                 "Denkmalart": denkmalart,
#                                                 "Denkmalname": denkmalname,
#                                                 "Sachbegriff": sachbegriff}

#                     resolved.append({"file": file, "dir": directory,
#                                      "vorgang": vorgang,
#                                      "vorhaben": vorhaben,
#                                      "hida": hida,
#                                      "obj": obj})
#         resolved_col.delete_many({})
#         resolved_col.insert_many(resolved)
    # logEntry(resolved)


def projectMetaDataFromHida(metadataname: str, hidaname: str):
    hida_col = mydb[hidaname]
    metadata_col = mydb[metadataname]
    for doc in metadata_col.find():
        if "hidas" in doc:
            hida = {}
            sachbegriff = set([])
            denkmalart = set([])
            denkmalname = set([])
            for hidaid in doc["hidas"]:
                hidaobj = hida_col.find_one(
                    {"OBJ-Dok-Nr": hidaid})
                if not hidaobj:
                    hidaobj = hida_col.find_one(
                        {"Teil-Obj-Dok-Nr": hidaid})
                if "Denkmalname" in hidaobj:
                    s = hidaobj["Denkmalname"]
                    denkmalname.update(s)

                if "Denkmalart" in hidaobj:
                    s: str = hidaobj["Denkmalart"]
                    denkmalart.add(s)

                sachbegriffh = hidaobj["Sachbegriff"]
                sachbegriff.update(sachbegriffh)

                hida[hidaid] = hidaobj
            metadata_col.update_one(
                {"_id": doc["_id"]}, {
                    "$set": {
                        # "hida": hida,
                        "Sachbegriff": list(sachbegriff),
                        "Denkmalart": list(denkmalart),
                        "Denkmalname": list(denkmalname)}
                })
        else:
            # hida = {}
            sachbegriff = set([])
            denkmalart = set([])
            denkmalname = set([])
            metadata_col.update_one(
                {"_id": doc["_id"]}, {
                    "$set": {
                        # "hida": hida,
                        "Sachbegriff": list(sachbegriff),
                        "Denkmalart": list(denkmalart),
                        "Denkmalname": list(denkmalname)}
                })


def setMetaDataDistrict(metadataname: str, district: str):
    metadata_col = mydb[metadataname]
    for doc in metadata_col.find():
        # if not "district" in doc:
        metadata_col.update_one(
            {"_id": doc["_id"]}, {
                "$set": {"district": district}
            })


def unsetMetaData(metadataname: str):
    # basically to save space in mongodb
    metadata_col = mydb[metadataname]
    for doc in metadata_col.find():
        if "meta" in doc:
            metadata_col.update_one(
                {"_id": doc["_id"]}, {
                    "$unset": {"meta": None,
                               "hida": None,
                               "text2": None}
                })


def incdocid(metadataname: str, inc: int):
    metadata_col = mydb[metadataname]
    for doc in metadata_col.find():
        if "docid" in doc:
            metadata_col.update_one(
                {"_id": doc["_id"]}, {
                    "$set": {"docid": doc["docid"]+inc}
                })
# incdocid("koepenick", 100000)


# def patchDir(resolvedname: str, folders: str, path: str):
#     folders_col = mydb[folders]
#     resolved_col = mydb[resolvedname]
#     for folder in folders_col.find():
#         for file in folder["files"]:
#             dir = folder["dir"]
#             dir = dir.replace(path, "")
#             f = file
#             if f.endswith(".doc"):
#                 f = f.replace(".doc", ".docx")
#             if f.endswith(".docx"):
#                 logEntry([dir, f])
#                 resolved_col.update_many(
#                     {"file": f}, {"$set": {"dir": dir}})


# def patchKeywords(resolvedname: str, topicsname: str):
#     topics_col = mydb[topicsname]
#     resolved_col = mydb[resolvedname]
#     for topic in topics_col.find():
#         # logEntry(topic["file"])
#         hidas = []
#         sachbegriff = []
#         denkmalart = []
#         denkmalname = []
#         if "hida" in topic:
#             for hida0 in topic["hida"]:
#                 hidas.append(hida0)
#                 # ????? weder hidas noch die attributaggregation wird weiter verwendet....
#                 sachbegriff += hida0["Sachbegriff"]
#                 denkmalart += hida0["Denkmalart"]
#                 denkmalname += hida0["Denkmalname"]

#         for theme in topic["keywords"]:
#             resolved_col.update_many(
#                 {"file": topic["file"]}, {"$set": {
#                     theme: topic["keywords"][theme]
#                 }})
#         # resolved_col.update_many(
#         #     {"file": topic["file"]}, {"$set": {
#         #         "html": topic["html"]
#         #     }})


def projectMetaDataKeywords(metadataname: str):
    col = mydb[metadataname]
    for doc in col.find():
        if "topic" in doc:
            topic = doc["topic"]
            logEntry(["projectMetaDataKeywords", doc["file"]])
            for theme in topic["keywords"]:
                col.update_many(
                    {"_id": doc["_id"]}, {"$set": {
                        theme: topic["keywords"][theme]
                    }})
        # resolved_col.update_many(
        #     {"file": topic["file"]}, {"$set": {
        #         "html": topic["html"]
        #     }})


def updateID(metadataname: str):
    col = mydb[metadataname]
    i = 0
    for doc in col.find():
        i += 1
        col.update_many(
            {"_id": doc["_id"]}, {"$set": {
                "docid": i
            }})


def unprojectMetaDataKeywords(metadataname: str):
    categories = []
    vorhabeninv_col = mydb["vorhaben_inv"]
    vorhabeninv = vorhabeninv_col.find()
    for v in vorhabeninv:
        for wor in v["words"]:
            if len(v["words"][wor]) == 0:
                categories.append(wor)
    col = mydb[metadataname]
    for doc in col.find():
        logEntry(["unprojectMetaDataKeywords", doc["file"]])
        for theme in categories:
            col.update_one({"_id": doc["_id"]}, {"$unset": {theme: None}})
        # if "topic" in doc:
        #     topic = doc["topic"]
        #     for theme in topic["keywords"]:
        #         col.update_one({"_id": doc["_id"]}, {"$unset": {theme: None}})


def patchText(resolvedname: str, textname: str):
    text_col = mydb[textname]
    resolved_col = mydb[resolvedname]
    for text in text_col.find():
        f = text["file"]
        t = text["text"]
        t = t.replace('\n', ' ')
        t = t.replace('\u2002', ' ')
        logEntry(text["file"])
        resolved_col.update_many(
            {"file": f}, {"$set": {
                "text": t
            }})


def projectHida(metadataname: str):
    resolved_col = mydb[metadataname]
    for reso0 in resolved_col.find():
        logEntry("projectHida: ", reso0["file"])
        hidas = []
        sachbegriff = []
        denkmalart = []
        denkmalname = []
        if "hida" in reso0:
            for hida0 in reso0["hida"]:
                hidas.append(hida0)
                if reso0["hida"][hida0]["Sachbegriff"]:
                    sachbegriff += reso0["hida"][hida0]["Sachbegriff"]
                if reso0["hida"][hida0]["Denkmalart"]:
                    denkmalart.append(reso0["hida"][hida0]["Denkmalart"])
                if reso0["hida"][hida0]["Denkmalname"]:
                    denkmalname += reso0["hida"][hida0]["Denkmalname"]
            resolved_col.update_one(
                {"file": reso0["file"]}, {
                    "$set": {"hidas": hidas, "Sachbegriff": list(set(sachbegriff)),
                             "Denkmalart": list(set(denkmalart)),
                             "Denkmalname": list(set(denkmalname))}
                })

###############################


def color_generator(number_of_colors):
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]
    return color


def patchCategories(words: str, categoriesname: str):
    categories = []
    if words in collist:
        vorhabeninv_col = mydb[words]
        vorhabeninv = vorhabeninv_col.find()
        for v in vorhabeninv:
            for wor in v["words"]:
                if len(v["words"][wor]) == 0:
                    categories.append(wor)
    catcolors = {}
    color = color_generator(len(categories))
    for i in range(len(categories)):
        catcolors[categories[i]] = {
            "color": color[i], "label": categories[i].upper()}

    cat_col = mydb[categoriesname]
    cat_col.delete_many({})
    cat_col.insert_one(catcolors)


def loadEmbddings(filename: str, colname: str):
    col: Collection = mydb[colname]
    items: any = []
    with open(filename, encoding='utf-8') as f:
        mlist = json.loads(f.read())
        for m in mlist:
            items.append({"word": m, "match": mlist[m], "correct": True})
    col.delete_many({})
    col.insert_many(items)


def loadNoMatches(filename: str, colname: str):
    col: Collection = mydb[colname]
    items: any = []
    with open(filename, encoding='utf-8') as f:
        mlist = json.loads(f.read())
        for m in mlist:
            items.append({"word": m, "count": mlist[m]})
    col.delete_many({})
    col.insert_many(items)


def projectInvTaxo(resolvedname: str, invtaxo: str):
    resolved_col = mydb[resolvedname]
    resol = resolved_col.find()
    for reso2 in resol:
        invtaxo_col = mydb[invtaxo]
        sblist = []
        if "Sachbegriff" in reso2:
            sblist = reso2["Sachbegriff"]
        if len(sblist) > 0:
            sl = sblist
            for sb in sblist:
                for plist in invtaxo_col.find({"name": sb}):
                    for pa in plist["parents"]:
                        if pa != "ARCHITEKTUR" and pa != "FUNKTION" and pa != "BAUAUFGABE" and not pa in sl:
                            sl.append(pa)
            resolved_col.update_one({"_id": reso2["_id"]}, {
                                    "$set": {"Sachbegriff": sl}})


def projectHidaInvTaxo(hidaname: str, invtaxo: str):
    hida_col = mydb[hidaname]
    invtaxo_col = mydb[invtaxo]
    hidal = hida_col.find()
    for hida in hidal:
        invtaxo_col = mydb["invtaxo"]
        sblist = hida["Sachbegriff"]
        if len(sblist) > 0:
            sl = sblist
            for sb in sblist:
                for plist in invtaxo_col.find({"name": sb}):
                    for pa in plist["parents"]:
                        if pa != "ARCHITEKTUR" and pa != "FUNKTION" and pa != "BAUAUFGABE" and not pa in sl:
                            sl.append(pa)
            hida_col.update_one({"_id": hida["_id"]}, {
                                "$set": {"Sachbegriff": sl}})


def initMongoFromStaticFiles(hidaname="hida",
                             ispattern=True,
                             isfolders=True,
                             isbadlist=True,
                             isvorhaben=True,
                             isvorhabeninv=True,
                             istaxo=False,
                             isinvtaxo=False,
                             iscategories=False,
                             ishida=False):
    if ispattern:
        loadArrayCollection(r".\static\pattern.json", "pattern")
    if ishida:
        with open(r".\static\hida.json", encoding='utf-8') as f:
            hida0: dict = json.loads(f.read())
            patchHida(hida0, hidaname)
    if isfolders:
        loadArrayCollection(r".\static\files.json", "folders")
        # loadArrayCollection("koepnick_files.json", "koepnick_folders")
        # loadArrayCollection("pankow_files.json", "pankow_folders")
        # loadArrayCollection("files.json", "folders")
    if isbadlist:
        loadArrayCollection(r".\static\badlist.json", "badlist")
    if isvorhaben:
        loadArrayCollection(r".\static\vorhaben.json", "vorhaben")
    if isvorhabeninv:
        loadDictCollection(r".\static\vorhaben_inv.json", "vorhaben_inv")
    if istaxo:
        loadArrayCollection(r".\static\taxo.json", "taxo")
    if isinvtaxo:
        loadArrayCollection(r".\static\taxo_inv.json", "invtaxo")
    if iscategories or isvorhabeninv:
        patchCategories(r".\static\vorhaben_inv", "categories")


def projectMetaData(metadataname="metadata",
                    hidaname="hida",
                    ismetadatahida=False,
                    ismetadatakeywords=False,
                    ismetadatanokeywords=False,
                    isupdatehida=False,
                    isupdatetaxo=False,
                    isupdatehidataxo=False):

    # isemblist=False,
    # isnoemblist=False,

    resetLog()

    # cleanup results from monument matcher
    if ismetadatahida:
        projectMetaDataFromHida(metadataname, hidaname)

    # remove keywords
    if ismetadatanokeywords:
        unprojectMetaDataKeywords(metadataname)

    # add keywords from extractintents, kw-list to document in order to filter by keyword
    if ismetadatakeywords:
        projectMetaDataKeywords(metadataname)

    # if istext:
    #     loadArrayCollection(r"..\static\text3.json", "text")

    # project from Hida: ["sachbegriff", "denkmalart", "denkmalname"]
    if isupdatehida:
        projectHida(metadataname)

    # if isupdatevorhaben:
    #     patchVorhaben(metadataname)

    # if isemblist:
    #     loadEmbddings(r".\static\all_matches.json", "emblist")

    # if isnoemblist:
    #     loadNoMatches(r".\static\no_matches.json", "noemblist")

    # add superclasses from Sachbegriff-Taxo to metadata
    if isupdatetaxo or ismetadatahida:
        projectInvTaxo(metadataname, "invtaxo")

    # add superclasses from Sachbegriff-Taxo to hida
    if isupdatehidataxo:
        projectHidaInvTaxo(hidaname, "invtaxo")

    resetLog()


# def lookupAddress(district: str, path: str):
#     r = requests.get("http://www.google.de/maps/place/" + "Berlin Treptow " + path, allow_redirects=True)
#     print(r.url)

# lookupAddress("Berlin Treptow", "moosdorfstrasse  7-9")


# body = { "name": "Treptow",
#         "metadataname": "treptow",
#         "district": "Treptow-Köpenick",
#         "path": "C:\\Data\\test\\KIbarDok\\Treptow\\1_Treptow",
#         "foldersname": "folders",
#         "tika": "http://localhost:9998",
#         "startindex": 0,
#         "dist": 0.5,
#         "corpus": "de_core_news_md",
#         "istika": False,
#         "issupport": False,
#         "isaddress": True,
#         "isdoctypes": False,
#         "isdates": False,
#         "istopic": False,
#         "isintents": False
# }

def extractMetaData(name: str,
                    metadataname: str,
                    district: str,
                    path: str,
                    foldersname: str,
                    tika: str,
                    startindex: number,
                    dist: float,
                    s2v: bool,
                    corpus: str,
                    istika=False,
                    isfolders=False,
                    issupport=False,
                    isaddress=False,
                    isdoctypes=False,
                    isdates=False,
                    istopic=False,
                    isintents=False,
                    ):

    resetLog()

    # if isexport:
    #     istaxo = (not "taxo" in collist)
    #     isinvtaxo = (not "invtaxo" in collist)
    #     isvorhaben = (not "vorhaben" in collist)
    #     isvorhaben_inv = (not "vorhaben_inv" in collist)
    #     ispattern = (not "pattern" in collist)
    #     isbadlist = (not "badlist" in collist)
    #     mongoExport(
    #         istaxo=istaxo,
    #         isinvtaxo=isinvtaxo,
    #         isbadlist=isbadlist,
    #         isvorhaben=isvorhaben,
    #         isvorhabeninv=isvorhaben_inv,
    #         ispattern=ispattern)

    hida = mydb["hida"]
    support = mydb["support"]

    metadata = mydb[metadataname]
    if istika:
        if not is_cancelled():
            tikaText(name, path, metadata, tika, startindex, True)

    if isfolders:
        if not is_cancelled():
            insertArrayCollection(getFolders(path), foldersname)

    if issupport:
        if not is_cancelled():
            initSupport(support, hida, district, district + "_streetnames")

    if isaddress:
        if not is_cancelled():
            findAddresses(metadata, support, "de", district + "_streetnames")
        folders = mydb[foldersname]
        if not is_cancelled():
            folderAddress(folders, hida, path, support, "de",
                          district, district + "_streetnames")
        if not is_cancelled():
            findMonuments(metadata, hida, support, folders, "de",
                          district, district + "_streetnames")
        if not is_cancelled():
            projectMetaData(metadataname=metadataname, ismetadatahida=True)

    if isdoctypes:
        if not "doctypes" in collist:
            doctypes = mydb["doctypes"]
            if not is_cancelled():
                initDocumentPattern(doctypes)
        doctypes = mydb["doctypes"]
        if not is_cancelled():
            findDocType(metadata, doctypes)
            # findDocTypeSpacy(metadata)

    if isdates:
        if not is_cancelled():
            findDates(metadata)

    if istopic:
        if not is_cancelled():
            findProject(metadata)

    if isintents:
        vorhabeninv_col = mydb["vorhaben_inv"]
        pattern_col = mydb["pattern"]
        badlist_col = mydb["badlist"]
        all_col = mydb["emblist"]
        no_col = mydb["noemblist"]
        if not is_cancelled():
            extractintents(metadata, vorhabeninv_col, pattern_col,
                           badlist_col, all_col, no_col, dist, corpus, s2v)
        if not is_cancelled():
            projectMetaData(metadataname=metadataname, ismetadatakeywords=True)

    resetLog()


# extractMetaData("Lichtenberg", "lichtenberg", "Lichtenberg",
#                 "E:\4_Lichtenberg",
#                 "lichtenberg_folders", "http://localhost:9998",0)
# extractMetaData("Treptow", "treptow", "Treptow-Köpenick",
#                 "C:\\Data\\test\\KIbarDok\\Treptow\\1_Treptow",
#                 "folders", "http://localhost:9998",0)
# extractMetaData("Treptow", "metadata", "Treptow-Köpenick",
#                 "C:\\Data\\test\\KIbarDok\\Treptow\\1_Treptow",
#                 "folders", "http://localhost:9998",0)
# extractMetaData("Köpenick", "koepenick", "Treptow-Köpenick",
#                "E:\\2_Köpenick",
#                 "koepnick_folders", "http://localhost:9998", 100000)
# extractMetaData("Mitte", "mitte", "Mitte",
#                "E:\5_Mitte",
#                 "mitte_folders", "http://localhost:9998", 200000)
# extractMetaData("Charlottenburg", "charlottenburg", "Charlottenburg-Wilmersdorf",
#                "E:\6_CharlottenburgWilmersdorf",
#                 "charlottenburg_folders", "http://localhost:9998", 200000)

# extractMetaData("Treptow", "metadata", "Treptow-Köpenick",
#                 "C:\\Data\\test\\KIbarDok\\Treptow\\1_Treptow","folders", "http://localhost:9998",0,0.8,True,"de_core_news_md",False,False,False,False,False,False,False,True)
# doctypes = mydb["doctypes"]
# initDocumentPattern(doctypes)
# findDocType(mydb["metadata"],mydb["doctypes"])
# findDocTypeSpacy(mydb["metadata"])



# updateID("metadata2")
# setMetaDataDistrict("lichtenberg","Lichtenberg")
# mongoExport(ismetadatanokeywords=True)

def extractText(metadataname: str, corpus: str):
    vorhabeninv_col = mydb["vorhaben_inv"]
    pattern_col = mydb["pattern"]
    badlist_col = mydb["badlist"]
    metadata = mydb[metadataname]
    extractTexts(metadata, vorhabeninv_col, pattern_col,
                 badlist_col,  metadataname, corpus)
# extractText("pankow", "de_core_news_md")
# extractText("lichtenberg", "de_core_news_md")
# extractText("mitte", "de_core_news_md")
# extractText("charlottenburg", "de_core_news_md")
# extractText("edg", "de_core_news_md")


    # with open(name, 'w') as fp:
    #     json.dump(ents, fp, indent=4, ensure_ascii=False)

# insertArrayCollection(getFolders("E:\\3_Pankow"), "pankow_folders")
# insertArrayCollection(getFolders("E:\\4_Lichtenberg"), "lichtenberg_folders")
# extractMetaData("Pankow", "pankow", "Pankow",
#                 "E:\\3_Pankow",
#                 "pankow_folders", "http://localhost:9998", 200000)

# cloneCollection("pankow", os.getenv("MONGO_CONNECTION_AZURE"), "kibardoc", "pankow")
# cloneCollection("pankow_folders", os.getenv("MONGO_CONNECTION_AZURE"), "kibardoc", "pankow_folders")
# unsetMetaData("metadata")
# unsetMetaData("koepenick")
# unsetMetaData("pankow")
# unsetMetaData("lichtenberg")

# uri2 =  os.getenv("MONGO_CONNECTION_PANKOW")
# cloneDatabase(uri2,"kibardoc",["metadata","folders",
#                                "treptow","treptow_folders",
#                                "koepenick", "koepenick_folders"
#                                ])
# uri2 =  os.getenv("MONGO_CONNECTION_TREPTOW")
# cloneDatabase(uri2,"kibardoc",["pankow","pankow_folders"])

# exportLocations(mydb["metadata"],mydb["location"])
# findLocations(mydb["metadata"])
# findaLocation(mydb["metadata"])