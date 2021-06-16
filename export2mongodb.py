# import spacy
import pymongo
import json

from pymongo.collection import Collection
# import os
from intent import extractTopicsAndPlaces, prepareWords, preparePattern
# import asyncio
# from bson.objectid import ObjectId
import random
from typing import Dict, Any, List, Tuple
from dotenv import load_dotenv

load_dotenv()
# uri = os.getenv("MONGO_CONNECTION")
uri = "mongodb+srv://klsuser:Kb.JHQ-.HrCs6Fw@cluster0.7qi8s.mongodb.net/test?authSource=admin&replicaSet=atlas-o1jpuq-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
# uri = "mongodb+srv://semtation:SemTalk3!@cluster0.pumvg.mongodb.net/kibardoc?retryWrites=true&w=majority"
# uri = "mongodb://localhost:27017"

myclient = pymongo.MongoClient(uri)
myclient._topology_settings

mydb = myclient["kibardoc"]
collist = mydb.list_collection_names()


def color_generator(number_of_colors):
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]
    return color


def loadArrayCollection(filename: str, colname: str):
    col: Collection = mydb[colname]
    items: any = []
    with open(filename, encoding='utf-8') as f:
        items = json.loads(f.read())
    col.delete_many({})
    col.insert_many(items)

def loadDictCollection(filename: str, colname: str):
    col: Collection = mydb[colname]
    item: any = {}
    with open(filename, encoding='utf-8') as f:
        item = json.loads(f.read())
    col.delete_many({})
    col.insert_one(item)

def patchHida(filename: str, hidaname: str):
    with open(filename, encoding='utf-8') as f:
        hida0: Dict = json.loads(f.read())
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


def patchResolved(resolvedname: str, filename: str, hidaname: str):
    hida_col = mydb[hidaname]
    resolved_col = mydb[resolvedname]
    with open(filename, encoding='utf-8') as f:
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
                    if len(vorhaben) == 1:
                        if vorhaben[0] == "Errichtung einer Mega-Light-Werbeanlage":
                            vorhaben = []
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
                                        hidaobj = hida_col.find_one(
                                            {"OBJ-Dok-Nr": hidaid})
                                        listentext = hidaobj["Listentext"]
                                        denkmalname = hidaobj["Denkmalname"]
                                        denkmalart = hidaobj["Denkmalart"]
                                        sachbegriff = hidaobj["Sachbegriff"]
                                        hida[hidaid] = {
                                            "hidaid": hidaid,
                                            "Listentext": listentext,
                                            "Denkmalart": denkmalart,
                                            "Denkmalname": denkmalname,
                                            "Sachbegriff": sachbegriff}
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
                                            hidaobj = hida_col.find_one(
                                                {"OBJ-Dok-Nr": hidaid})
                                            listentext = hidaobj["Listentext"]
                                            denkmalname = hidaobj["Denkmalname"]
                                            denkmalart = hidaobj["Denkmalart"]
                                            sachbegriff = hidaobj["Sachbegriff"]
                                            hida[hidaid] = {
                                                "hidaid": hidaid,
                                                "Listentext": listentext,
                                                "Denkmalart": denkmalart,
                                                "Denkmalname": denkmalname,
                                                "Sachbegriff": sachbegriff}

                    resolved.append({"file": file, "dir": directory,
                                     "vorgang": vorgang,
                                     "vorhaben": vorhaben,
                                     "hida": hida,
                                     "obj": obj})
        resolved_col.delete_many({})
        resolved_col.insert_many(resolved)
        # print(resolved)


def patchDir(resolvedname: str, folders: str, path: str):
    folders_col = mydb[folders]
    resolved_col = mydb[resolvedname]
    for folder in folders_col.find():
        for file in folder["files"]:
            dir = folder["dir"]
            dir = dir.replace(path, "")
            f = file
            if f.endswith(".doc"):
                f = f.replace(".doc", ".docx")
            if f.endswith(".docx"):
                print(dir, f)
                resolved_col.update_many(
                    {"file": f}, {"$set": {"dir": dir}})


def patchKeywords(resolvedname: str, topicsname: str):
    topics_col = mydb[topicsname]
    resolved_col = mydb[resolvedname]
    for topic in topics_col.find():
        # print(topic["file"])
        hidas = []
        sachbegriff = []
        denkmalart = []
        denkmalname = []
        if "hida" in topic:
            for hida0 in topic["hida"]:
                hidas.append(hida0)
                sachbegriff += hida0["Sachbegriff"]
                denkmalart += hida0["Denkmalart"]
                denkmalname += hida0["Denkmalname"]

        for theme in topic["keywords"]:
            resolved_col.update_many(
                {"file": topic["file"]}, {"$set": {
                    theme: topic["keywords"][theme]
                }})
        # resolved_col.update_many(
        #     {"file": topic["file"]}, {"$set": {
        #         "html": topic["html"]
        #     }})


def patchText(resolvedname: str, textname: str):
    text_col = mydb[textname]
    resolved_col = mydb[resolvedname]
    for text in text_col.find():
        f = text["file"]
        t = text["text"]
        t = t.replace('\n', ' ')
        t = t.replace('\u2002', ' ')
        print(text["file"])
        resolved_col.update_many(
            {"file": f}, {"$set": {
                "text": t
            }})


def projectHida(resolvedname: str):
    resolved_col = mydb[resolvedname]
    for reso0 in resolved_col.find():
        print(reso0["file"])
        hidas = []
        sachbegriff = []
        denkmalart = []
        denkmalname = []
        if "hida" in reso0:
            for hida0 in reso0["hida"]:
                hidas.append(hida0)
                sachbegriff += reso0["hida"][reso0]["Sachbegriff"]
                denkmalart.append(reso0["hida"][reso0]["Denkmalart"])
                denkmalname += reso0["hida"][reso0]["Denkmalname"]
            resolved_col.update_one(
                {"file": reso0["file"]}, {
                    "$set": {"hidas": hidas, "Sachbegriff": list(set(sachbegriff)),
                             "Denkmalart": list(set(denkmalart)),
                             "Denkmalname": list(set(denkmalname))}
                })


def patchVorhaben(resolvedname: str):
    resolved_col = mydb[resolvedname]
    for reso1 in resolved_col.find():
        if "vorhaben" in reso1 and len(reso1["vorhaben"]) == 1 and reso1["vorhaben"][0] == 'Errichtung einer Mega-Light-Werbeanlage':
            print(reso1["file"])
            resolved_col.update_one(
                {"file": reso1["file"]}, {
                    "$set": {"vorhaben": []}
                })


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


def patchInvTaxo(resolvedname: str, invtaxo: str):
    resolved_col = mydb[resolvedname]
    resol = resolved_col.find()
    for reso2 in resol:
        invtaxo_col = mydb[invtaxo]
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


def mongoExport(ispattern=False, ishida=False, isresolved=False,
                isfolders=False, isbadlist=False,
                isvorhaben=False, isvorhabeninv=False,
                istaxo=False, istopics=False,
                ispatch_dir=False, iskeywords=False,
                isupdatehida=False, isupdatevorhaben=False,
                istext=False, isupdatetext=False,
                iscategories=False,
                isemblist=False, isnoemblist=False,
                isinvtaxo=False, isupdatetaxo=False,
                isupdatehidataxo=False):
    if ispattern:
        loadArrayCollection("pattern.json", "pattern")

    if ishida:
        patchHida("hida.json", "hida")

    if isresolved:
        patchResolved("resolved", "resolved.json", "hida")

    if isfolders:
        loadArrayCollection("files.json", "folders")

    if isbadlist:
        loadArrayCollection("badlist.json", "badlist")

    if isvorhaben:
        loadArrayCollection("vorhaben.json", "vorhaben")

    if isvorhabeninv:
        loadDictCollection("vorhaben_inv.json", "vorhaben_inv")

    if istaxo:
        loadArrayCollection("taxo.json", "taxo")

    if istopics:
        loadArrayCollection("topics3a.json", "topics")

    if ispatch_dir or isresolved:
        patchDir("resolved", "folders", r"C:\Data\test\KIbarDok")

    if isresolved or istopics or iskeywords:
        patchKeywords("resolved", "topics")

    if istext:
        loadArrayCollection("text3.json", "text")

    if isresolved or isupdatetext:
        patchText("resolved", "text")

    if isresolved or isupdatehida:
        projectHida("resolved")

    if isresolved or isupdatevorhaben:
        patchVorhaben("resolved")

    if iscategories or isvorhabeninv:
        patchCategories("vorhaben_inv", "categories")

    if isemblist:
        loadEmbddings("all_matches.json", "emblist")

    if isnoemblist:
        loadNoMatches("no_matches.json", "noemblist")

    if isinvtaxo:
        loadArrayCollection("taxo_inv.json", "invtaxo")

    if isresolved or isupdatetaxo:
        patchInvTaxo("resolved", "invtaxo")

    if ishida or isupdatehidataxo:
        projectHidaInvTaxo("hida", "invtaxo")

# mongoExport(ispattern=True,ishida=True,isresolved=True,isfolders=True,isbadlist=True,isvorhaben=True,
        #    isvorhabeninv=True, istaxo=True,istopics=True, ispatch_dir=True, iskeywords=True)
# mongoExport(iskeywords=True)
# mongoExport(isresolved=True)
# mongoExport(istext=True)
# mongoExport(isupdatetext=True)
# mongoExport(istopics=True)
# mongoExport(isfolders=True,isbadlist=True,iscategories=True,isvorhaben=True)
# mongoExport(isupdatevorhaben=True)
# mongoExport(isvorhabeninv=True)
# mongoExport(isemblist=True)
# mongoExport(isnoemblist=True)
# mongoExport(isinvtaxo=True)
# mongoExport(isupdatetaxo=True)
# mongoExport(isupdatehidataxo=True)
# mongoExport(iscategories=True)
mongoExport(ispatch_dir=True)

def prepareList():
    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv: Dict = vorhabeninv_col.find_one()
        wvi: Dict[str, List[str]] = {}
        wvi = vorhabeninv["words"]
        # v: Dict[str,List[str]] = vorhabeninv["words"]
        # for wor in v:
        #     wvi[wor] = v[wor]

        words, wordlist = prepareWords(wvi)
        categories: List[str] = []
        # if "categories" in collist:
        #     cat_col = mydb["categories"]
        #     catobj = cat_col.find_one()
        #     for cat in catobj:
        #         if cat != '_id':
        #             categories.append(cat)

        patternjs: List[str] = []
        if "pattern" in collist:
            pattern_col = mydb["pattern"]
            pattern = pattern_col.find()
            for v in pattern:
                patternjs.append(v["paragraph"])
        plist: List[Dict[str, str]] = preparePattern(patternjs)

        badlistjs: List[str] = []
        if "badlist" in collist:
            badlist_col = mydb["badlist"]
            badlist = badlist_col.find()
            for v in badlist:
                badlistjs.append(v["paragraph"])

    return words, wordlist, categories, plist, badlistjs


def extractintents():

    words, wordlist, categories, plist, badlistjs = prepareList()

    bparagraph = True

    res = extractTopicsAndPlaces(
        words, wordlist, categories, plist, badlistjs, bparagraph, "")
    # topics_col = mydb["topics"]
    # topics_col.delete_many({})
    # topics_col.insert_many(res)
    return res

# extractintents()
