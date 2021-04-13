# import spacy
import pymongo
import json
# import os
from intent import extractTopicsAndPlaces, prepareWords, preparePattern
# import asyncio
from bson.objectid import ObjectId

uri = "mongodb+srv://semtation:SemTalk3!@cluster0.pumvg.mongodb.net/kibardoc?retryWrites=true&w=majority"
# uri = "mongodb://localhost:27017"

myclient = pymongo.MongoClient(uri)
myclient._topology_settings

mydb = myclient["kibardoc"]
collist = mydb.list_collection_names()

if not "pattern" in collist:
    pattern_col = mydb["pattern"]
    with open("pattern.json", encoding='utf-8') as f:
        pattern = json.loads(f.read())
    pattern_col.insert_many(pattern)

if not "hida" in collist:
    hida_col = mydb["hida"]
    with open("hida.json", encoding='utf-8') as f:
        hida = json.loads(f.read())
        monuments = []
        for hid in hida:
            monument = hida[hid]
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
    hida_col.insert_many(monuments)


if not "resolved" in collist:
   resolved_col = mydb["resolved"]
   hida_col = mydb["hida"]
   with open("resolved.json", encoding='utf-8') as f:
        resolvedjs = json.loads(f.read())
        resolved = []
        for directory in resolvedjs:
            el = resolvedjs[directory]
            if "datei" in el:
                filesjs = el["datei"]
                for file in filesjs:
                    # print(directory, file)
                    obj = filesjs[file]
                    vorhaben = obj["vorhaben"]
                    vorgang = obj["vorgang"]
                    objnr = obj["objnr"]
                    hida = {}
                    if "method" in objnr:
                        meth = objnr["method"]
                        if len(meth) > 0:
                            for o in objnr:
                                if o != "method" and o != "behoerde" and o != "hausnummer":
                                    if meth == 'inhalt_direct' and o == "treffer":
                                        treflist = objnr["treffer"][meth]
                                        tref = treflist[0]
                                        hidaid = tref[0]
                                        hidaobj = hida_col.find_one({ "OBJ-Dok-Nr": hidaid})
                                        listentext = hidaobj["Listentext"]
                                        denkmalname = hidaobj["Denkmalname"]
                                        denkmalart = hidaobj["Denkmalart"]
                                        sachbegriff = hidaobj["Sachbegriff"]
                                        hida[hidaid] = {
                                            "hidaid": hidaid, 
                                            "Listentext": listentext, 
                                            "Denkmalart": denkmalart, 
                                            "Denkmalname": denkmalname, 
                                            "Sachbegriff": sachbegriff, 
                                            "treffer": treflist}
                                        #     if isinstance(hidaobjl, list):
                                        #         for hidaid in hidaobjl:
                                        #             hida[hidaid]= { "hidaid": hidaid, "treffer": objnr["treffer"]}
                                        #     else:
                                        #             hida[hidaid]= { "hidaid": hidaobjl, "treffer": objnr["treffer"]}
                                    else:
                                        denkmal = objnr[o]
                                        # print(denkmal)
                                        for hidaobj in denkmal["treffer"][meth]:
                                            hidaid = hidaobj[0]
                                            hidaobj = hida_col.find_one({ "OBJ-Dok-Nr": hidaid})
                                            listentext = hidaobj["Listentext"]
                                            denkmalname = hidaobj["Denkmalname"]
                                            denkmalart = hidaobj["Denkmalart"]
                                            sachbegriff = hidaobj["Sachbegriff"]
                                            hida[hidaid] = {
                                                "hidaid": hidaid, 
                                                "Listentext": listentext, 
                                                "Denkmalart": denkmalart, 
                                                "Denkmalname": denkmalname, 
                                                "Sachbegriff": sachbegriff, 
                                                "treffer": hidaobj}

                    resolved.append({"file": file, "dir": directory,
                                     "vorgang": vorgang,
                                     "vorhaben": vorhaben,
                                     "hida": hida,
                                     "obj": obj})
        resolved_col.insert_many(resolved)
        print(resolved)

if not "folders" in collist:
    folders_col = mydb["folders"]
    with open("files.json", encoding='utf-8') as f:
        fileslist = json.loads(f.read())
    folders_col.insert_many(fileslist)

if not "badlist" in collist:
    badlist_col = mydb["badlist"]
    with open("badlist.json", encoding='utf-8') as f:
        fileslist = json.loads(f.read())
    badlist_col.insert_many(fileslist)

if not "vorhaben" in collist:
    vorhaben_col = mydb["vorhaben"]
    with open("vorhaben.json", encoding='utf-8') as f:
        vorhaben = json.loads(f.read())
    vorhaben_col.insert_many(vorhaben)

if not "vorhaben_inv" in collist:
    vorhabeninv_col = mydb["vorhaben_inv"]
    with open("vorhaben_inv.json", encoding='utf-8') as f:
        vorhabeninv = json.loads(f.read())
    vorhabeninv_col.insert_one(vorhabeninv)

if not "taxo" in collist:
    col = mydb["taxo"]
    with open("taxo.json", encoding='utf-8') as f:
        topics = json.loads(f.read())
    col.insert_many(topics)


def extractintents():

    wvi = {}

    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv = vorhabeninv_col.find()
        for v in vorhabeninv:
            for wor in v["words"]:
                wvi[wor] = v["words"][wor]
    words, wordlist = prepareWords(wvi)

    patternjs = []
    if "pattern" in collist:
        pattern_col = mydb["pattern"]
        pattern = pattern_col.find()
        for v in pattern:
            patternjs.append({"paragraph": v["paragraph"]})
    plist = preparePattern(patternjs)

    badlistjs = []
    if "badlist" in collist:
        badlist_col = mydb["badlist"]
        badlist = badlist_col.find()
        for v in badlist:
            badlistjs.append({"paragraph": v["paragraph"]})

    bparagraph = True

    res = extractTopicsAndPlaces(
        words, wordlist, plist, badlistjs, bparagraph, "")
    col = mydb["topics"]
    col.insert_many(res)
    return res

# if "topics" in collist:
#     col = mydb["topics"]
#     mydb.drop_collection(col)

# if not "topics" in collist:
#     extractintents()


if not "topics" in collist:
    col = mydb["topics"]
    with open("topics3a.json", encoding='utf-8') as f:
        topics = json.loads(f.read())
    col.insert_many(topics)

# if "resolved" in collist and "folders" in collist:
#     folders_col = mydb["folders"]
#     resolved_col = mydb["resolved"]
#     for folder in folders_col.find():
#         for file in folder["files"]:
#             dir = folder["dir"]
#             dir = dir.replace(r"C:\Data\test\KIbarDok","")
#             f = file
#             if f.endswith(".doc"):
#                 f = f.replace(".doc", ".docx")
#             if f.endswith(".docx"):
#                 print(dir,f)
#                 resolved_col.update_many(
#                     {"file": f}, {"$set": {"dir": dir}})

if "resolved" in collist and "topics" in collist:
    topics_col = mydb["topics"]
    resolved_col = mydb["resolved"]
    for topic in topics_col.find():
        resolved_col.update_many(
            {"file": topic["file"]}, {"$set": {
                "keywords": topic["keywords"]}})

# if "resolved" in collist and "hida" in collist:
#     hida_col = mydb["hida"]
#     resolved_col = mydb["resolved"]

#     for doc in resolved_col.find():
#         print(doc["file"])
#         for didid in doc["hida"]:
#             hida = hida_col.find_one({ "OBJ-Dok-Nr": didid})
#             listentext = hida["Listentext"]
#             denkmalname = hida["Denkmalname"]
#             denkmalart = hida["Denkmalart"]
#             sachbegriff = hida["Sachbegriff"]
#             resolved_col.update(
#                 {"file": doc["file"]}, {"$set": {"hida[].Listentext": listentext, "Denkmalart": denkmalart, "Denkmalname": denkmalname, "Sachbegriff": sachbegriff}})

# print(mydb.list_collection_names())

# taxo_col = mydb["taxo"]
# for taxo in taxo_col.find({'topic': 'Klostermauer'}):
#     print(taxo)

# hida_col = mydb["hida"]
# for mon in hida_col.find({"Bezirk": "Treptow-Köpenick"}, {"OBJ-Dok-Nr": 1, "Denkmalname": 1, "Sachbegriff": 1}):
#     if len(mon["Denkmalname"]) > 0:
#         if "Sachbegriff" in mon:
#             print(mon["OBJ-Dok-Nr"], mon["Denkmalname"][0], mon["Sachbegriff"])
#         else:
#             print(mon["OBJ-Dok-Nr"], mon["Denkmalname"][0])